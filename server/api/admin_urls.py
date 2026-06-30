from django.urls import include, path

urlpatterns = [
    path("clients/", include("apps.clients.admin_urls")),
    path('', include('apps.staff.admin_urls')),
]