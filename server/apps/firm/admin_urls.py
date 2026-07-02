from django.urls import path

from apps.firm.views.admin.admin_firm_settings_view import AdminFirmSettingsView
from apps.firm.views.admin.admin_firm_view import AdminFirmDetailView

urlpatterns = [
    path("settings/", AdminFirmSettingsView.as_view(), name="admin-firm-settings"),
    path("", AdminFirmDetailView.as_view(), name="admin-firm-detail"),
]