from rest_framework import status
from rest_framework.response import Response

from apps.staff.serializers.secretary import SecretaryCaseSerializer
from apps.staff.services.secretary import SecretaryCaseService
from apps.staff.views.secretary.secretary_base_view import SecretaryBaseView


class SecretaryCasesView(SecretaryBaseView):
    def get(self, request):
        try:
            cases = SecretaryCaseService.list_cases(request.user)
        except (ValueError, PermissionError) as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_403_FORBIDDEN)

        serializer = SecretaryCaseSerializer(cases, many=True)
        return Response({"cases": serializer.data}, status=status.HTTP_200_OK)
