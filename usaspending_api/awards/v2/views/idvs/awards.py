from collections import OrderedDict
from copy import deepcopy

from django.db import connection
from psycopg2.sql import Identifier, Literal, SQL
from rest_framework.request import Request
from rest_framework.response import Response

from usaspending_api.awards.award_id_helper import detect_award_id_type, AwardIdType
from usaspending_api.common.cache_decorator import cache_response
from usaspending_api.common.helpers.generic_helper import get_simple_pagination_metadata
from usaspending_api.common.views import APIDocumentationView
from usaspending_api.core.validator.pagination import PAGINATION
from usaspending_api.core.validator.tinyshield import TinyShield
from usaspending_api.etl.broker_etl_helpers import dictfetchall


# Columns upon which the client is allowed to sort.
SORTABLE_COLUMNS = (
    'award_type',
    'description',
    'funding_agency',
    'last_date_to_order',
    'obligated_amount',
    'period_of_performance_current_end_date',
    'period_of_performance_start_date',
    'piid',
)

DEFAULT_SORT_COLUMN = 'period_of_performance_start_date'

GET_IDVS_SQL = SQL("""
    select
        ac.id                                      award_id,
        ac.type_description                        award_type,
        ac.description,
        tf.funding_agency_name                     funding_agency,
        ac.generated_unique_award_id,
        tf.ordering_period_end_date                last_date_to_order,
        pac.rollup_total_obligation                obligated_amount,
        ac.period_of_performance_current_end_date,
        ac.period_of_performance_start_date,
        ac.piid
    from
        parent_award pap
        inner join parent_award pac on pac.parent_award_id = pap.award_id
        inner join awards ac on ac.id = pac.award_id
        inner join transaction_fpds tf on tf.transaction_id = ac.latest_transaction_id
    where
        pap.{award_id_column} = %s
    order by
        {sort_column} {sort_direction}, ac.id {sort_direction}
    limit {limit} offset {offset}
""")

GET_CONTRACTS_SQL = SQL("""
    select
        ac.id                                      award_id,
        ac.type_description                        award_type,
        ac.description,
        tf.funding_agency_name                     funding_agency,
        ac.generated_unique_award_id,
        tf.ordering_period_end_date                last_date_to_order,
        ac.total_obligation                        obligated_amount,
        ac.period_of_performance_current_end_date,
        ac.period_of_performance_start_date,
        ac.piid
    from
        parent_award pap
        inner join awards ap on ap.id = pap.award_id
        inner join awards ac on ac.fpds_parent_agency_id = ap.fpds_agency_id and ac.parent_award_piid = ap.piid and
            ac.type not like 'IDV\_%%'
        inner join transaction_fpds tf on tf.transaction_id = ac.latest_transaction_id
    where
        pap.{award_id_column} = %s
    order by
        {sort_column} {sort_direction}, ac.id {sort_direction}
    limit {limit} offset {offset}
""")


def _prepare_tiny_shield_rules():
    """
    Our TinyShield rules never change.  Encapsulate them here and store them
    once in TINY_SHIELD_RULES.
    """

    # This endpoint supports paging.
    models = deepcopy(PAGINATION)

    # Add the list of sortable columns for validation.
    sort_rule = TinyShield.get_model_by_name(models, 'sort')
    sort_rule['type'] = 'enum'
    sort_rule['enum_values'] = SORTABLE_COLUMNS
    sort_rule['default'] = DEFAULT_SORT_COLUMN

    # Add additional models for the award id and the idv filter.
    models.extend([
        # Award id can be either an integer or a string depending upon whether
        # it's an internal id or a unique generated id.
        {'key': 'award_id', 'name': 'award_id', 'type': 'any', 'optional': False, 'models': [
            {'type': 'integer'},
            {'type': 'text', 'text_type': 'search'}
        ]},
        {'key': 'idv', 'name': 'idv', 'type': 'boolean', 'default': True, 'optional': True}
    ])

    return models


TINY_SHIELD_RULES = _prepare_tiny_shield_rules()


class IDVAwardsViewSet(APIDocumentationView):
    """Returns the direct children of an IDV.
    endpoint_doc: /awards/idvs/awards.md
    """

    @staticmethod
    def _parse_and_validate_request(request: Request) -> dict:
        return TinyShield(deepcopy(TINY_SHIELD_RULES)).block(request)

    @staticmethod
    def _business_logic(request_data: dict) -> list:
        award_id, award_id_type = detect_award_id_type(request_data['award_id'])
        award_id_column = 'award_id' if award_id_type is AwardIdType.internal else 'generated_unique_award_id'
        sql = GET_IDVS_SQL if request_data['idv'] else GET_CONTRACTS_SQL
        sql = sql.format(
            award_id_column=Identifier(award_id_column),
            award_id=Literal(award_id),
            sort_column=Identifier(request_data['sort']),
            sort_direction=SQL(request_data['order']),
            limit=Literal(request_data['limit'] + 1),
            offset=Literal((request_data['page'] - 1) * request_data['limit']),
        )
        with connection.cursor() as cursor:
            cursor.execute(sql, [award_id])
            return dictfetchall(cursor)

    @cache_response()
    def post(self, request: Request) -> Response:
        request_data = self._parse_and_validate_request(request.data)
        results = self._business_logic(request_data)
        page_metadata = get_simple_pagination_metadata(len(results), request_data['limit'], request_data['page'])

        response = OrderedDict((
            ('results', results[:request_data['limit']]),
            ('page_metadata', page_metadata)
        ))

        return Response(response)
