from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.common.choices import UserRole


class AdminSecretaryBaseView(APIView):
    permission_classes = [IsAuthenticated]

    def get_law_firm(self):
        user = self.request.user

        if user.role != UserRole.ADMIN:
            raise PermissionDenied("Only admins can manage secretaries.")

        if hasattr(user, "owned_firm"):
            return user.owned_firm

        raise PermissionDenied("Admin is not attached to a law firm.")
