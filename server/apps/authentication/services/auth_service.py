from django.contrib.auth import authenticate

from rest_framework_simplejwt.tokens import RefreshToken

from apps.firms.models import LawFirmMember


class AuthService:

    @staticmethod
    def login_user(email: str, password: str):
        user = authenticate(
            username=email,
            password=password,
        )

        if not user:
            return None, "Invalid credentials"

        membership = (
            LawFirmMember.objects
            .select_related("firm")
            .filter(
                user=user,
                is_active=True,
            )
            .first()
        )

        firm = membership.firm if membership else None
        firm_role = membership.role if membership else None

        refresh = RefreshToken.for_user(user)

        return {
            "user": user,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "role": user.role,
            "firm": firm,
            "firm_role": firm_role,
        }, None

    @staticmethod
    def logout_user(refresh_token: str):
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return True, None
        except Exception:
            return False, "Invalid refresh token"