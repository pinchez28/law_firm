from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.staff.serializers.staff_detail_serializer import (
    StaffDetailSerializer,
)
from apps.staff.services.staff_service import StaffService


class AdminActivateLawyerView(APIView):
    """
    Activate a lawyer.
    """

    def post(self, request, lawyer_id):
        lawyer = StaffService.get_staff(
            staff_id=lawyer_id,
            law_firm=request.user.staff_profile.law_firm,
        )

        lawyer = StaffService.activate_staff(
            staff=lawyer,
            updated_by=request.user,
        )

        return Response(
            StaffDetailSerializer(lawyer).data,
            status=status.HTTP_200_OK,
        )