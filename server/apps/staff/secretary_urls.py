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
    path("", AdminStaffListView.as_view(firm_role=FirmRole.SECRETARY), name="admin-secretary-list"),
    path("create/", AdminStaffCreateView.as_view(firm_role=FirmRole.SECRETARY), name="admin-secretary-create"),
    path("<uuid:staff_id>/", AdminStaffDetailView.as_view(firm_role=FirmRole.SECRETARY), name="admin-secretary-detail"),
    path("<uuid:staff_id>/update/", AdminStaffUpdateView.as_view(firm_role=FirmRole.SECRETARY), name="admin-secretary-update"),
    path("<uuid:staff_id>/delete/", AdminStaffDeleteView.as_view(firm_role=FirmRole.SECRETARY), name="admin-secretary-delete"),
    path("<uuid:staff_id>/activate/", AdminStaffActivateView.as_view(firm_role=FirmRole.SECRETARY), name="admin-secretary-activate"),
    path("<uuid:staff_id>/deactivate/", AdminStaffDeactivateView.as_view(firm_role=FirmRole.SECRETARY), name="admin-secretary-deactivate"),
    path("<uuid:staff_id>/change-status/", AdminStaffChangeStatusView.as_view(firm_role=FirmRole.SECRETARY), name="admin-secretary-change-status"),
]
