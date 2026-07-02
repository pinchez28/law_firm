from django.urls import path

from apps.common.choices import FirmRole
from apps.staff.views.admin.staff_base import (
    AdminStaffActivateView,
    AdminStaffChangeStatusView,
    AdminStaffCreateView,
    AdminStaffDeactivateView,
    AdminStaffDeleteView,
    AdminStaffDetailView,
    AdminStaffListView,
    AdminStaffUpdateView,
)

urlpatterns = [
    path("", AdminStaffListView.as_view(firm_role=FirmRole.HR), name="admin-hr-list"),
    path("create/", AdminStaffCreateView.as_view(firm_role=FirmRole.HR), name="admin-hr-create"),
    path("<uuid:staff_id>/", AdminStaffDetailView.as_view(firm_role=FirmRole.HR), name="admin-hr-detail"),
    path("<uuid:staff_id>/update/", AdminStaffUpdateView.as_view(firm_role=FirmRole.HR), name="admin-hr-update"),
    path("<uuid:staff_id>/delete/", AdminStaffDeleteView.as_view(firm_role=FirmRole.HR), name="admin-hr-delete"),
    path("<uuid:staff_id>/activate/", AdminStaffActivateView.as_view(firm_role=FirmRole.HR), name="admin-hr-activate"),
    path("<uuid:staff_id>/deactivate/", AdminStaffDeactivateView.as_view(firm_role=FirmRole.HR), name="admin-hr-deactivate"),
    path("<uuid:staff_id>/change-status/", AdminStaffChangeStatusView.as_view(firm_role=FirmRole.HR), name="admin-hr-change-status"),
]
