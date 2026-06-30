from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.staff.serializers.staff_change_status_serializer import (
    StaffChangeStatusSerializer,
)
from apps.staff.serializers.staff_detail_serializer import (
    StaffDetailSerializer,
)
from apps.staff.services.staff_service import StaffService


class AdminChangeLawyerStatusView(APIView):
    """
    Change a lawyer's employment status.
    """

    def post(self, request, lawyer_id):
        lawyer = StaffService.get_staff(
            staff_id=lawyer_id,
            law_firm=request.user.staff_profile.law_firm,
        )

        serializer = StaffChangeStatusSerializer(
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)

        lawyer = StaffService.change_employment_status(
            staff=lawyer,
            status=serializer.validated_data["employment_status"],
            reason=serializer.validated_data.get("termination_reason"),
            updated_by=request.user,
        )

        return Response(
            StaffDetailSerializer(lawyer).data,
            status=status.HTTP_200_OK,
        )