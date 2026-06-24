from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.clients.serializers.individual_client_create_serializer import (
    IndividualClientCreateSerializer,
)

from apps.clients.services.individual_client_service import (
    IndividualClientService,
)

from apps.clients.serializers.client_serializer import (
    ClientSerializer,
)


class IndividualClientCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        serializer = IndividualClientCreateSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        client = IndividualClientService.create_client(
            validated_data=serializer.validated_data,
            user=request.user,
        )

        response_serializer = ClientSerializer(client)

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
        )