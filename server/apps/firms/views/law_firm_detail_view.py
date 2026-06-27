from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from apps.firms.models import LawFirm
from apps.firms.serializers.law_firm_serializer import (
    LawFirmSerializer,
)


class LawFirmDetailView(RetrieveAPIView):

    serializer_class = LawFirmSerializer

    permission_classes = [
        IsAuthenticated,
    ]

    def get_object(self):
        return self.request.user.owned_firm