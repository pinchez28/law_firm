from rest_framework import status
from rest_framework.response import Response

from apps.staff.serializers.secretary import SecretaryClientSerializer
from apps.staff.services.secretary import SecretaryClientService
from apps.staff.views.secretary.secretary_base_view import SecretaryBaseView


class SecretaryClientsView(SecretaryBaseView):
    def get(self, request):
        try:
            clients = SecretaryClientService.list_clients(request.user)
        except (ValueError, PermissionError) as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_403_FORBIDDEN)

        serializer = SecretaryClientSerializer(clients, many=True)
        return Response({"clients": serializer.data}, status=status.HTTP_200_OK)
