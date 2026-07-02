from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from apps.firm.services.firm_settings_service import FirmSettingService
from apps.firm.serializers.firm_settings_serializer import FirmSettingSerializer


class AdminFirmSettingsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        firm = request.user.owned_firm
        settings = FirmSettingService.get_settings(firm)
        serializer = FirmSettingSerializer(settings)
        return Response(serializer.data)

    def patch(self, request):
        firm = request.user.owned_firm
        settings = FirmSettingService.get_settings(firm)

        serializer = FirmSettingSerializer(
            settings,
            data=request.data,
            partial=True
        )

        serializer.is_valid(raise_exception=True)
        updated = FirmSettingService.update_settings(
            firm=firm,
            validated_data=serializer.validated_data
        )

        return Response(FirmSettingSerializer(updated).data)