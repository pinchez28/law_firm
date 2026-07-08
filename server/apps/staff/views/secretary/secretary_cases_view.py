from rest_framework import status
from rest_framework.response import Response

from apps.staff.serializers.secretary import SecretaryCaseSerializer
from apps.staff.services.secretary import SecretaryCaseService
from apps.staff.views.secretary.secretary_base_view import SecretaryBaseView


class SecretaryCasesView(SecretaryBaseView):
    def get(self, request, case_id=None):
        try:
            if case_id is not None:
                case = SecretaryCaseService.get_case(request.user, case_id)
                if case is None:
                    return Response(
                        {"detail": "Case not found."},
                        status=status.HTTP_404_NOT_FOUND,
                    )
                serializer = SecretaryCaseSerializer(case)
                return Response({"case": serializer.data}, status=status.HTTP_200_OK)

            cases = SecretaryCaseService.list_cases(request.user)
        except (ValueError, PermissionError) as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_403_FORBIDDEN)

        serializer = SecretaryCaseSerializer(cases, many=True)
        return Response({"cases": serializer.data}, status=status.HTTP_200_OK)
