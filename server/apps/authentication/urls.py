from django.urls import path

from .views.login_view import LoginView
from .views.logout_view import LogoutView
from .views.register_view import RegisterFirmView
from .views.change_password_view import ChangePasswordView

urlpatterns = [
    path("register-firm/", RegisterFirmView.as_view(), name="register-firm"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
]