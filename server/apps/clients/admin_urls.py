from django.urls import path

from .views.client_admin_assign_view import ClientAdminAssignView
from .views.client_admin_dashboard_view import ClientAdminDashboardView
from .views.client_admin_delete_view import ClientAdminDeleteView
from .views.client_admin_detail_view import ClientAdminDetailView
from .views.client_admin_lawyers_view import ClientAdminLawyersView
from .views.client_admin_list_view import ClientAdminListView
from .views.client_admin_remove_lawyer_view import ClientAdminRemoveLawyerView
from .views.client_admin_statistics_view import ClientAdminStatisticsView
from .views.client_admin_status_view import ClientAdminStatusView

urlpatterns = [
    path("", ClientAdminListView.as_view(), name="admin-client-list"),
    path("dashboard/", ClientAdminDashboardView.as_view(), name="admin-client-dashboard"),
    path("statistics/", ClientAdminStatisticsView.as_view(), name="admin-client-statistics"),
    path("<uuid:client_id>/", ClientAdminDetailView.as_view(), name="admin-client-detail"),
    path("<uuid:client_id>/activate/", ClientAdminStatusView.as_view(), name="admin-client-activate"),
    path("<uuid:client_id>/deactivate/", ClientAdminStatusView.as_view(), name="admin-client-deactivate"),
    path("<uuid:client_id>/change-status/", ClientAdminStatusView.as_view(), name="admin-client-change-status"),
    path("<uuid:client_id>/lawyers/", ClientAdminLawyersView.as_view(), name="admin-client-lawyers"),
    path("<uuid:client_id>/assign-lawyer/", ClientAdminAssignView.as_view(), name="admin-client-assign-lawyer"),
    path("<uuid:client_id>/remove-lawyer/<uuid:lawyer_id>/", ClientAdminRemoveLawyerView.as_view(), name="admin-client-remove-lawyer"),
    path("<uuid:client_id>/delete/", ClientAdminDeleteView.as_view(), name="admin-client-delete"),
]