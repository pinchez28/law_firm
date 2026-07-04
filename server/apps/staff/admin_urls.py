from django.urls import include, path

urlpatterns = [
    path("lawyers/", include("apps.staff.lawyer_admin_urls")),
]
