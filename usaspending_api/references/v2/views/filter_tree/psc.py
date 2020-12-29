from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from usaspending_api.common.cache_decorator import cache_response
from usaspending_api.common.validator.tinyshield import TinyShield
from usaspending_api.references.v2.views.filter_tree.psc_filter_tree import PSCFilterTree


class PSCViewSet(APIView):
    """
    Returns a list of PSC search tree nodes, with populated children if depth > 0.
    """

    endpoint_doc = "usaspending_api/api_contracts/contracts/v2/references/filter_tree/psc.md"

    def _parse_and_validate(self, request):
        models = [
            {"key": "depth", "name": "depth", "type": "integer", "allow_nulls": True, "default": 0, "optional": True},
            {
                "key": "filter",
                "name": "filter",
                "type": "text",
                "text_type": "search",
                "allow_nulls": True,
                "optional": True,
                "default": None,
            },
        ]
        return TinyShield(models).block(request)

    @cache_response()
    def get(self, request: Request, tier1: str = None, tier2: str = None, tier3: str = None) -> Response:
        request_values = self._parse_and_validate(request.GET)

        filter_tree = PSCFilterTree()
        return Response(
            {"results": filter_tree.search(tier1, tier2, tier3, request_values["depth"], request_values["filter"])}
        )
