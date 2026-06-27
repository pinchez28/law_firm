from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.firms.serializers.law_firm_create_serializer import (
    LawFirmCreateSerializer,
)

from apps.firms.serializers.law_firm_serializer import (
    LawFirmSerializer,
)

from apps.firms.services.law_firm_service import (
    LawFirmService,
)


class LawFirmCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = LawFirmCreateSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        firm = LawFirmService.create_firm(
            validated_data=serializer.validated_data,
            owner=request.user,
        )

        return Response(
            LawFirmSerializer(firm).data,
            status=status.HTTP_201_CREATED,
        )