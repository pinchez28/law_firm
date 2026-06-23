from rest_framework.response import Response
from rest_framework.views import APIView

from apps.clients.models.client import ClientType


class ClientTypesView(APIView):

    def get(self, request):

        return Response(
            [
                {
                    "value": value,
                    "label": label,
                }
                for value, label in ClientType.choices
            ]
        )