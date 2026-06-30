from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.staff.serializers.staff_create_serializer import StaffCreateSerializer
from apps.staff.serializers.staff_detail_serializer import StaffDetailSerializer
from apps.staff.services.staff_service import StaffService
from apps.common.choices import FirmRole


class AdminCreateLawyerView(APIView):
    """
    Create a new lawyer for the authenticated user's law firm.
    """

    def post(self, request):
        data = request.data.copy()

        # Force the staff role for this endpoint.
        data["firm_role"] = FirmRole.ASSOCIATE

        serializer = StaffCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        lawyer = StaffService.create_staff(
            law_firm=request.user.staff_profile.law_firm,
            validated_data=serializer.validated_data,
            created_by=request.user,
        )

        return Response(
            StaffDetailSerializer(lawyer).data,
            status=status.HTTP_201_CREATED,
        )