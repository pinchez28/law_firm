from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.staff.serializers.staff_detail_serializer import (
    StaffDetailSerializer,
)
from apps.staff.serializers.staff_update_serializer import (
    StaffUpdateSerializer,
)
from apps.staff.services.staff_service import StaffService


class AdminUpdateLawyerView(APIView):
    """
    Update a lawyer.
    """

    def patch(self, request, lawyer_id):
        lawyer = StaffService.get_staff(
            staff_id=lawyer_id,
            law_firm=request.user.staff_profile.law_firm,
        )

        serializer = StaffUpdateSerializer(
            lawyer,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        lawyer = StaffService.update_staff(
            staff=lawyer,
            validated_data=serializer.validated_data,
            updated_by=request.user,
        )

        return Response(
            StaffDetailSerializer(lawyer).data,
            status=status.HTTP_200_OK,
        )