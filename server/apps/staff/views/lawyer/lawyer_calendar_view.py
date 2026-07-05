from rest_framework import status
from rest_framework.response import Response

from apps.staff.views.lawyer.lawyer_base_view import LawyerBaseView


class LawyerCalendarView(LawyerBaseView):
    def get(self, request):
        try:
            self.get_lawyer()
        except PermissionError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_403_FORBIDDEN)

        return Response(
            {
                "events": [
                    {
                        "id": "evt-001",
                        "title": "Court hearing",
                        "start": "2026-07-10T09:00:00Z",
                        "end": "2026-07-10T10:00:00Z",
                    }
                ]
            },
            status=status.HTTP_200_OK,
        )
