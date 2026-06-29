from django.urls import path
from . views.client_list_view import ClientListView

urlpatterns = [
    path("", ClientListView.as_view(), name="admin-client-list"),
]