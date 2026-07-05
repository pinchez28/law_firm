from rest_framework import status
from rest_framework.response import Response

from apps.staff.services.lawyer.lawyer_password_service import LawyerPasswordService
from apps.staff.views.lawyer.lawyer_base_view import LawyerBaseView


class LawyerChangePasswordView(LawyerBaseView):
    def post(self, request):
        current_password = request.data.get("current_password")
        new_password = request.data.get("new_password")
        confirm_password = request.data.get("confirm_password")

        if not current_password or not new_password or not confirm_password:
            return Response({"detail": "All password fields are required."}, status=status.HTTP_400_BAD_REQUEST)

        if new_password != confirm_password:
            return Response({"detail": "New passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            LawyerPasswordService.change_password(request.user, current_password, new_password)
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "Password updated successfully."}, status=status.HTTP_200_OK)
