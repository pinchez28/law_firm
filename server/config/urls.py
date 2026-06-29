from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/firms/', include('apps.firms.urls')),
    path('api/auth/', include('apps.authentication.urls')),
    path('api/clients/', include('apps.clients.urls')),
    # path('api/staff/', include('apps.staff.urls')),
    
]
