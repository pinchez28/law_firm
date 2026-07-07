from apps.staff.models import SecretaryPermission


class SecretaryCaseService:
    @staticmethod
    def list_cases(user):
        secretary = getattr(user, "secretary_profile", None)
        if secretary is None:
            raise ValueError("Only secretaries can access this endpoint.")

        if not secretary.has_permission(SecretaryPermission.MANAGE_CASES):
            raise PermissionError("Admin permission is required to manage cases.")

        return [
            {
                "id": "case-001",
                "title": "Sample matter filing",
                "case_number": "SC-2026-001",
                "status": "OPEN",
                "client_name": "Sample Client",
                "assigned_lawyer": "Assigned Lawyer",
                "next_action": "Prepare filing documents",
                "last_updated": "2026-07-06T00:00:00Z",
            }
        ]
