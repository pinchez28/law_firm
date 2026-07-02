from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.firm.models import LawFirm
from apps.firm.serializers.firm_serializer import LawFirmSerializer
from apps.firm.services.firm_service import FirmService   


class AdminFirmDetailView(APIView):
    """
    Admin endpoint to view current firm information.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        firm = LawFirm.objects.select_related("owner").get(
            owner=request.user
        )

        serializer = LawFirmSerializer(firm)
        return Response(serializer.data)
    
    def patch(self, request):
        firm = request.user.owned_firm

        serializer = LawFirmSerializer(
            firm,
            data=request.data,
            partial=True
        )

        serializer.is_valid(raise_exception=True)

        # update via service (clean separation)
        updated_firm = FirmService.update_firm(
            firm=firm,
            validated_data=serializer.validated_data
        )

        return Response(LawFirmSerializer(updated_firm).data)