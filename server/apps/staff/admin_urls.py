from django.urls import include, path

urlpatterns = [
    path("lawyers/", include("apps.staff.lawyer_admin_urls")),
    path("secretaries/", include("apps.staff.secretary_admin_urls")),
]
