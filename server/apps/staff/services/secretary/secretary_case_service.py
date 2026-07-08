from apps.staff.models import SecretaryPermission
from apps.cases.services import CaseService


class SecretaryCaseService:
    @staticmethod
    def list_cases(user):
        secretary = getattr(user, "secretary_profile", None)
        if secretary is None:
            raise ValueError("Only secretaries can access this endpoint.")

        if not secretary.has_permission(SecretaryPermission.MANAGE_CASES):
            raise PermissionError("Admin permission is required to manage cases.")

        return CaseService.list_cases(user)

    @classmethod
    def get_case(cls, user, case_id):
        try:
            return CaseService.get_case(user, case_id)
        except Exception:
            return None
