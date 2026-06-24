from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.clients.serializers.company_client_create_serializer import CompanyClientCreateSerializer

from apps.clients.services.company_client_service import CompanyClientService

from apps.clients.serializers.client_serializer import ClientSerializer


class CompanyClientCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        # ----------------------------------
        # 1. Validate request
        # ----------------------------------
        serializer = CompanyClientCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # ----------------------------------
        # 2. Create via service layer
        # ----------------------------------
        client = CompanyClientService.create_client(
            validated_data=serializer.validated_data,
            user=request.user,
        )

        # ----------------------------------
        # 3. Response serialization
        # ----------------------------------
        response_serializer = ClientSerializer(client)

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
        )