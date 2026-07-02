from django.urls import include, path

urlpatterns = [
    path("lawyers/", include("apps.staff.lawyer_urls")),
    path("secretaries/", include("apps.staff.secretary_urls")),
    path("accountants/", include("apps.staff.accountant_urls")),
    path("hr/", include("apps.staff.hr_urls")),
    path("it/", include("apps.staff.it_urls")),
    path("office-assistants/", include("apps.staff.office_assistant_urls")),
]