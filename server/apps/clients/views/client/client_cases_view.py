from rest_framework import status
from rest_framework.response import Response

from apps.clients.serializers.client.client_case_serializer import ClientCaseSerializer
from apps.clients.services.client.client_case_service import ClientCaseService
from apps.clients.views.client.client_base_view import ClientBaseView


class ClientCasesView(ClientBaseView):
    def get(self, request):
        try:
            client = request.user.client_profile
        except Exception:
            return Response({"detail": "Only clients can access this endpoint."}, status=status.HTTP_403_FORBIDDEN)

        serializer = ClientCaseSerializer(ClientCaseService.list_cases(client), many=True)
        return Response({"cases": serializer.data}, status=status.HTTP_200_OK)
