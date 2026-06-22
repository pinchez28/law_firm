from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from ..serializers.login_serializer import LoginSerializer
from ..services.auth_service import AuthService


class LoginView(APIView):
    """
    Handles user login and returns JWT tokens + user info.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result, error = AuthService.login_user(
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
        )

        if error:
            return Response(
                {"detail": error},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        user = result["user"]

        return Response(
            {
                "access": result["access"],
                "refresh": result["refresh"],
                "user": {
                    "id": str(user.id),
                    "email": user.email,
                    "role": user.role,
                    "full_name": user.full_name,
                },
            },
            status=status.HTTP_200_OK,
        )