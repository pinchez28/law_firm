from django.urls import path

from .views.admin.lawyers.admin_lawyer_list_view import AdminLawyerListView
from .views.admin.lawyers.admin_create_lawyer_view import AdminCreateLawyerView
from .views.admin.lawyers.admin_lawyer_detail_view import AdminLawyerDetailView
from .views.admin.lawyers.admin_update_lawyer_view import AdminUpdateLawyerView
from .views.admin.lawyers.admin_delete_lawyer_view import AdminDeleteLawyerView
from .views.admin.lawyers.admin_activate_lawyer_view import AdminActivateLawyerView
from .views.admin.lawyers.admin_deactivate_lawyer_view import AdminDeactivateLawyerView


urlpatterns = [
    # Lawyer Management
    path(
        "lawyers/",
        AdminLawyerListView.as_view(),
        name="admin-lawyer-list",
    ),
    path(
        "lawyers/create/",
        AdminCreateLawyerView.as_view(),
        name="admin-lawyer-create",
    ),

    # Individual Lawyer
    path(
        "lawyers/<uuid:lawyer_id>/",
        AdminLawyerDetailView.as_view(),
        name="admin-lawyer-detail",
    ),
    path(
        "lawyers/<uuid:lawyer_id>/update/",
        AdminUpdateLawyerView.as_view(),
        name="admin-lawyer-update",
    ),
    path(
        "lawyers/<uuid:lawyer_id>/delete/",
        AdminDeleteLawyerView.as_view(),
        name="admin-lawyer-delete",
    ),

    # Status Management
    path(
        "lawyers/<uuid:lawyer_id>/activate/",
        AdminActivateLawyerView.as_view(),
        name="admin-lawyer-activate",
    ),
    path(
        "lawyers/<uuid:lawyer_id>/deactivate/",
        AdminDeactivateLawyerView.as_view(),
        name="admin-lawyer-deactivate",
    ),
]