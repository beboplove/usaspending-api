from django.urls import include, path, re_path
from usaspending_api.agency.v2.views.agency_overview import AgencyOverview
from usaspending_api.agency.v2.views.program_activity_count import ProgramActivityCount
from usaspending_api.agency.v2.views.federal_account_count import FederalAccountCount


urlpatterns = [
    re_path(
        "(?P<toptier_code>[0-9]{3,4})/",
        include([path("", AgencyOverview.as_view()), path("program_activity/count/", ProgramActivityCount.as_view())]),
    ),
    re_path(
        "(?P<toptier_code>[0-9]{3,4})/",
        include([path("", AgencyOverview.as_view()), path("federal_account/count/", FederalAccountCount.as_view())]),
    ),
]
