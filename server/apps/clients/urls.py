from django.urls import path

from apps.clients.views.client_onboarding_view import ClientOnboardingView

from .views import (
    ClientListCreateView,
    ClientDetailView,
    ClientTypesView,
)

from .views.individual_client_create_view import IndividualClientCreateView
from .views.company_client_create_view import CompanyClientCreateView

urlpatterns = [
    path(
        "types/",
        ClientTypesView.as_view(),
        name="client-types",
    ),

    path(
        "",
        ClientListCreateView.as_view(),
        name="client-list-create",
    ),

    path(
        "<uuid:client_id>/",
        ClientDetailView.as_view(),
        name="client-detail",
    ),

    path("onboard/", ClientOnboardingView.as_view()),


    # CLIENT SUBTYPE ENDPOINTS
    # Individual clients creation
    path(
        "individual/",
        IndividualClientCreateView.as_view(),
        name="create-individual-client"
    ),

    
    # Company clients creation
    path(
        "company/",
        CompanyClientCreateView.as_view(),
        name="create-company-client"
    ),

    # # NGO clients creation
    # path(
    #     "ngo/",
    #     NgoClientCreateView.as_view(),
    #     name="create-ngo-client"
    # ),

    # # Trust clients creation
    # path(
    #     "trust/",
    #     TrustClientCreateView.as_view(),
    #     name="create-trust-client"
    # ),

    # # Government clients creation
    # path(
    #     "government/",
    #     GovernmentClientCreateView.as_view(),
    #     name="create-governement-client"
    # ),

    # # Partnership clients creation
    # path(
    #     "partnership/",
    #     PartnershipClientCreateView.as_view(),
    #     name="create-partnership-client"
    # ),
]