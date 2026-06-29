from django.urls import include, path

urlpatterns = [
    path("auth/", include("apps.authentication.admin_urls")),
    # path("staff/", include("apps.staff.admin_urls")),
    # path("firms/", include("apps.firms.admin_urls")),
]