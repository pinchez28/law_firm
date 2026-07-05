from rest_framework import status
from rest_framework.response import Response

from apps.staff.views.lawyer.lawyer_base_view import LawyerBaseView


class LawyerTasksView(LawyerBaseView):
    def get(self, request):
        try:
            self.get_lawyer()
        except PermissionError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_403_FORBIDDEN)

        return Response(
            {
                "tasks": [
                    {
                        "id": "task-001",
                        "title": "Prepare draft pleadings",
                        "due_date": "2026-07-08",
                        "status": "PENDING",
                    }
                ]
            },
            status=status.HTTP_200_OK,
        )
