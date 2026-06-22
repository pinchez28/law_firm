from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from ..services.auth_service import AuthService


class LogoutView(APIView):
    """
    Blacklists refresh token to log user out.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response(
                {"detail": "Refresh token is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        success, error = AuthService.logout_user(refresh_token)

        if not success:
            return Response(
                {"detail": error},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {"detail": "Logged out successfully"},
            status=status.HTTP_200_OK,
        )