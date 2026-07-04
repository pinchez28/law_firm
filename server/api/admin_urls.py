from django.urls import include, path

urlpatterns = [
    path("firm/", include("apps.firm.admin_urls")),
    path("staff/", include("apps.staff.admin_urls")),
]
