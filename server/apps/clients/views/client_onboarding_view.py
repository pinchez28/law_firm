from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from apps.clients.serializers import ClientSerializer
from apps.clients.serializers.client_onboarding_serializer import (
    ClientOnboardingSerializer
)
from apps.clients.services.client_onboarding_service import (
    ClientOnboardingService
)


class ClientOnboardingView(APIView):

    permission_classes = [IsAuthenticated]  # IMPORTANT for safety

    def post(self, request):

        # -----------------------------
        # 1. VALIDATE INPUT CONTRACT
        # -----------------------------
        serializer = ClientOnboardingSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)

        # -----------------------------
        # 2. CALL ONBOARDING ENGINE
        # -----------------------------
        client = ClientOnboardingService.onboard(
            validated_data=serializer.validated_data,
            user=request.user
        )

        # -----------------------------
        # 3. RESPONSE SERIALIZATION
        # -----------------------------
        response_data = ClientSerializer(client).data

        return Response(
            response_data,
            status=status.HTTP_201_CREATED
        )