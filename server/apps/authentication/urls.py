from django.urls import path

from .views.login_view import LoginView
from .views.logout_view import LogoutView
from .views.register_view import RegisterFirmView

urlpatterns = [
    path("register-firm/", RegisterFirmView.as_view(), name="register-firm"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]