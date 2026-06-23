from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.clients.serializers import (
    ClientSerializer,
    ClientUpdateSerializer,
)

from apps.clients.services import (
    ClientService,
)


class ClientDetailView(APIView):

    def get(self, request, client_id):

        client = ClientService.get_client_by_id(
            client_id
        )

        serializer = ClientSerializer(
            client
        )

        return Response(serializer.data)

    def patch(self, request, client_id):

        client = ClientService.get_client_by_id(
            client_id
        )

        serializer = ClientUpdateSerializer(
            client,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(
            raise_exception=True
        )

        client = ClientService.update_client(
            client,
            **serializer.validated_data
        )

        return Response(
            ClientSerializer(client).data
        )

    def delete(self, request, client_id):

        client = ClientService.get_client_by_id(
            client_id
        )

        ClientService.delete_client(client)

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )