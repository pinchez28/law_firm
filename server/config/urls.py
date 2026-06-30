from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    path("api/auth/", include("apps.authentication.urls")),

    path("api/admin/", include("api.admin_urls")),
    path("api/lawyer/", include("api.lawyer_urls")),
]