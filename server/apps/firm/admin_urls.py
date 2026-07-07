from django.urls import path

from apps.firm.views.admin.admin_department_detail_view import AdminDepartmentDetailView
from apps.firm.views.admin.admin_department_list_view import AdminDepartmentListView
from apps.firm.views.admin.admin_firm_settings_view import AdminFirmSettingsView
from apps.firm.views.admin.admin_firm_view import AdminFirmDetailView

urlpatterns = [
    path("departments/", AdminDepartmentListView.as_view(), name="admin-firm-departments"),
    path("departments/<uuid:department_id>/", AdminDepartmentDetailView.as_view(), name="admin-firm-department-detail"),
    path("settings/", AdminFirmSettingsView.as_view(), name="admin-firm-settings"),
    path("", AdminFirmDetailView.as_view(), name="admin-firm-detail"),
]
