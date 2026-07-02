from django.urls import include, path

# urlpatterns = [
#     path("clients/", include("apps.clients.admin_urls")),
#     path('', include('apps.staff.admin_urls')),
# ]

urlpatterns = [
    path("firm/", include("apps.firm.admin_urls")),
]