from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.staff.services.staff_service import StaffService


class AdminDeleteLawyerView(APIView):
    """
    Delete (deactivate) a lawyer.
    """

    def delete(self, request, lawyer_id):
        lawyer = StaffService.get_staff(
            staff_id=lawyer_id,
            law_firm=request.user.staff_profile.law_firm,
        )

        StaffService.delete_staff(
            staff=lawyer,
            deleted_by=request.user,
        )

        return Response(
            {
                "detail": "Lawyer deleted successfully."
            },
            status=status.HTTP_204_NO_CONTENT,
        )