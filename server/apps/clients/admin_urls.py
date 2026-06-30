from django.urls import path

from .views.client_list_view import ClientListView
from .views.client_detail_view import ClientDetailView

urlpatterns = [
    path("", ClientListView.as_view()),
    path("<uuid:client_id>/", ClientDetailView.as_view()),
    # path("<uuid:client_id>/archive/", ArchiveClientView.as_view()),
    # path("<uuid:client_id>/restore/", RestoreClientView.as_view()),
    # path("<uuid:client_id>/documents/", ClientDocumentsView.as_view()),
    # path("<uuid:client_id>/cases/", ClientCasesView.as_view()),
]