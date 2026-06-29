from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    path("api/auth/", include("api.auth_urls")),

    path("api/admin/", include("api.admin_urls")),
    # path("api/staff/", include("api.staff_urls")),
    # path("api/client/", include("api.client_urls")),
]