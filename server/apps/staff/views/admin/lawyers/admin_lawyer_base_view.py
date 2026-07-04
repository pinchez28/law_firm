from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.common.choices import UserRole


class AdminLawyerBaseView(APIView):
    permission_classes = [IsAuthenticated]

    def get_law_firm(self):
        user = self.request.user

        if user.role != UserRole.ADMIN:
            raise PermissionDenied("Only admins can manage lawyers.")

        if hasattr(user, "owned_firm"):
            return user.owned_firm

        if hasattr(user, "lawyer_profile"):
            return user.lawyer_profile.law_firm

        raise PermissionDenied("Admin is not attached to a law firm.")