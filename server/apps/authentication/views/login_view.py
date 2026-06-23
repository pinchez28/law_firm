from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from apps.authentication.serializers.login_serializer import LoginSerializer
from apps.users.serializers.user_serializer import UserSerializer
from apps.authentication.services.auth_service import AuthService


class LoginView(APIView):
    """
    Handles user login and returns JWT tokens + serialized user info.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        # 1. Validate input
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 2. Authenticate user via service layer
        result, error = AuthService.login_user(
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
        )

        # 3. Handle authentication failure
        if error:
            return Response(
                {"detail": error},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        user = result["user"]

        # 4. Return clean, serialized response
        return Response(
            {
                "access": result["access"],
                "refresh": result["refresh"],
                "user": UserSerializer(user).data,
            },
            status=status.HTTP_200_OK,
        )