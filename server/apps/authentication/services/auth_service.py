from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


# ==========================================================
# AUTH SERVICE
# ==========================================================
class AuthService:
    @staticmethod
    def login_user(email: str, password: str):
        user = authenticate(username=email, password=password)

        if not user:
            return None, "Invalid credentials"

        refresh = RefreshToken.for_user(user)

        return {
            "user": user,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }, None
    
    @staticmethod
    def logout_user(refresh_token: str):
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return True, None
        except Exception:
            return False, "Invalid refresh token"
    



