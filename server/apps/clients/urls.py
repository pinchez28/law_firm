from django.urls import path

from .views import (
    ClientListView,
    ClientDetailView,
    IndividualClientCreateView,
    CompanyClientCreateView,
)

urlpatterns = [
    # Client List Endpoint
    path(
        "",
        ClientListView.as_view(),
        name="client-list",
    ),

    # Client Detail Endpoint
    path(
        "<uuid:client_id>/",
        ClientDetailView.as_view(),
        name="client-detail",
    ),
    # Individual Client Creation Endpoint
    path(
        "individuals/",
        IndividualClientCreateView.as_view(),
        name="create-individual-client",
    ),
    # Company Client Creation Endpoint
    path(
        "companies/",
        CompanyClientCreateView.as_view(),
        name="create-company-client",
    ),
]