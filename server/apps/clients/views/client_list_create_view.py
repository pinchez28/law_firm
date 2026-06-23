from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.clients.serializers import (
    ClientSerializer,
    ClientCreateSerializer,
)

from apps.clients.services import ClientService


class ClientListCreateView(APIView):

    def get(self, request):

        clients = ClientService.get_all_clients()

        serializer = ClientSerializer(
            clients,
            many=True,
        )

        return Response(serializer.data)

    def post(self, request):

        serializer = ClientCreateSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        client = ClientService.create_client(
            **serializer.validated_data
        )

        response_serializer = ClientSerializer(
            client
        )

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
        )