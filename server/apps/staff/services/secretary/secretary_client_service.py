from apps.staff.models import SecretaryPermission


class SecretaryClientService:
    @staticmethod
    def list_clients(user):
        secretary = getattr(user, "secretary_profile", None)
        if secretary is None:
            raise ValueError("Only secretaries can access this endpoint.")

        if not secretary.can_manage_client_intake and not secretary.has_permission(
            SecretaryPermission.MANAGE_CLIENTS
        ):
            raise PermissionError("Admin permission is required to manage clients.")

        return [
            {
                "id": "client-001",
                "full_name": "Sample Client",
                "client_type": "INDIVIDUAL",
                "phone_number": "0700000000",
                "email": "client@example.com",
                "lifecycle_status": "PROSPECT",
                "last_updated": "2026-07-06T00:00:00Z",
            }
        ]
