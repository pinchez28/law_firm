from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.staff.serializers.staff_serializer import StaffSerializer
from apps.staff.services.staff_service import StaffService
from apps.common.choices import FirmRole


class AdminLawyerListView(APIView):
    """
    List all lawyers belonging to the authenticated user's law firm.
    """

    def get(self, request):
        lawyers = StaffService.list_staff(
            law_firm=request.user.staff_profile.law_firm,
            firm_role=FirmRole.ASSOCIATE,
        )

        serializer = StaffSerializer(
            lawyers,
            many=True,
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )