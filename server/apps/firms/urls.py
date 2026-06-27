from django.urls import path

from apps.firms.views.law_firm_create_view import (
    LawFirmCreateView,
)

from apps.firms.views.law_firm_detail_view import (
    LawFirmDetailView,
)

urlpatterns = [
    path(
        "",
        LawFirmCreateView.as_view(),
        name="firm-create",
    ),

    path(
        "me/",
        LawFirmDetailView.as_view(),
        name="firm-detail",
    ),
]