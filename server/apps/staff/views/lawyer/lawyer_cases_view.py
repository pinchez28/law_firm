from rest_framework import status
from rest_framework.response import Response

from apps.staff.serializers.lawyer.lawyer_case_serializer import LawyerCaseSerializer
from apps.staff.services.lawyer.lawyer_case_service import LawyerCaseService
from apps.staff.views.lawyer.lawyer_base_view import LawyerBaseView


class LawyerCasesView(LawyerBaseView):
    def get(self, request):
        try:
            cases = LawyerCaseService.list_cases(request.user)
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_403_FORBIDDEN)

        serializer = LawyerCaseSerializer(cases, many=True)
        return Response({"cases": serializer.data}, status=status.HTTP_200_OK)
