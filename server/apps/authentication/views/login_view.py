from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from ..services.auth_service import AuthService


class LoginView(APIView):

    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        result, error = AuthService.login_user(
            email=email,
            password=password,
        )

        if error:
            return Response(
                {"detail": error},
                status=status.HTTP_401_UNAUTHORIZED
            )

        user = result["user"]
        firm = result["firm"]

        return Response({
            "access": result["access"],
            "refresh": result["refresh"],

            "user": {
                "id": user.id,
                "email": user.email,
                "full_name": f"{user.first_name} {user.last_name}",
                "role": result["role"],
            },

            "firm": {
                "id": firm.id if firm else None,
                "name": firm.name if firm else None,
            },

            "firm_role": result["firm_role"],
        }, status=status.HTTP_200_OK)