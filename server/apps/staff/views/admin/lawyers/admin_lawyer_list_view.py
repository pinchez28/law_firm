from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.staff.serializers.staff_serializer import StaffSerializer
from apps.staff.services.staff_service import StaffService


class AdminLawyerListView(APIView):

    def get(self, request):
        result = StaffService.list_staff(
            law_firm=request.user.staff_profile.law_firm,
        )

        lawyers = result["queryset"]
        analytics = result["analytics"]

        serializer = StaffSerializer(lawyers, many=True)

        return Response(
            {
                # 🔥 FULL FIRM ANALYTICS (centralized)
                "summary": analytics.get_dashboard(),

                # 🔥 DATA
                "lawyers": serializer.data,

                # 🔥 META INFO
                "metadata": {
                    "total_records": lawyers.count(),
                },
            },
            status=status.HTTP_200_OK,
        )