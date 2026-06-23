from django.urls import path

from .views import (
    ClientListCreateView,
    ClientDetailView,
    ClientTypesView,
)

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
]