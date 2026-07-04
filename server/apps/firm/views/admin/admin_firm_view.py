from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.firm.models import LawFirm
from apps.firm.serializers.firm_serializer import LawFirmSerializer
from apps.firm.services.firm_service import FirmService
from apps.firm.services.firm_analytics_service import FirmAnalyticsService


class AdminFirmDetailView(APIView):
    """
    Admin endpoint to view and update the current law firm.
    """

    permission_classes = [IsAuthenticated]

    PROTECTED_FIELDS = {
        "id",
        "owner",
        "owner_email",
        "owner_name",
        "created_at",
    }

    def get(self, request):
        firm = LawFirm.objects.select_related("owner").get(
            owner=request.user
        )

        return Response({
            "firm": LawFirmSerializer(firm).data,
            "analytics": FirmAnalyticsService.get_firm_summary(firm=firm),
        })

    def patch(self, request):
        firm = request.user.owned_firm

        protected = self.PROTECTED_FIELDS.intersection(request.data.keys())

        if protected:
            return Response(
                {
                    "detail": "The following fields cannot be updated.",
                    "fields": sorted(protected),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = LawFirmSerializer(
            firm,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(raise_exception=True)

        updated_firm = FirmService.update_firm(
            firm=firm,
            validated_data=serializer.validated_data,
        )

        return Response(
            LawFirmSerializer(updated_firm).data,
            status=status.HTTP_200_OK,
        )