from apps.staff.views.staff_workspace_views import (
    StaffWorkspaceChangePasswordView,
    StaffWorkspaceDashboardView,
    StaffWorkspaceItemsView,
    StaffWorkspaceProfileView,
)


class ITProfileView(StaffWorkspaceProfileView):
    profile_attr = "it_profile"
    role_label = "IT"


class ITDashboardView(StaffWorkspaceDashboardView):
    profile_attr = "it_profile"
    role_label = "IT"
    default_work = staticmethod(
        lambda profile: {
            "can_manage_users": profile.can_manage_users,
            "can_manage_system_settings": profile.can_manage_system_settings,
            "can_manage_security": profile.can_manage_security,
            "can_access_audit_logs": profile.can_access_audit_logs,
        }
    )


class ITChangePasswordView(StaffWorkspaceChangePasswordView):
    profile_attr = "it_profile"
    role_label = "IT"


class ITTasksView(StaffWorkspaceItemsView):
    profile_attr = "it_profile"
    role_label = "IT"
    item_type = "task"
    response_key = "tasks"


class ITDocumentsView(StaffWorkspaceItemsView):
    profile_attr = "it_profile"
    role_label = "IT"
    item_type = "document"
    response_key = "documents"


class ITCalendarView(StaffWorkspaceItemsView):
    profile_attr = "it_profile"
    role_label = "IT"
    item_type = "calendar-event"
    response_key = "calendar"


class ITNotificationsView(StaffWorkspaceItemsView):
    profile_attr = "it_profile"
    role_label = "IT"
    item_type = "notification"
    response_key = "notifications"


class ITSystemsView(StaffWorkspaceItemsView):
    profile_attr = "it_profile"
    role_label = "IT"
    item_type = "system"
    response_key = "systems"


__all__ = [
    "ITCalendarView",
    "ITChangePasswordView",
    "ITDashboardView",
    "ITDocumentsView",
    "ITNotificationsView",
    "ITProfileView",
    "ITSystemsView",
    "ITTasksView",
]
