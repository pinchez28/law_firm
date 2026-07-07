class LawyerCaseService:
    @staticmethod
    def list_cases(user):
        if not hasattr(user, "lawyer_profile"):
            raise ValueError("Only lawyers can access this endpoint.")

        return [
            {
                "id": "11111111-1111-1111-1111-111111111111",
                "title": "Sample litigation matter",
                "case_number": "LC-2026-001",
                "status": "ACTIVE",
                "client_name": "Acme Holdings",
                "practice_area": "Litigation",
                "assigned_lawyer": user.lawyer_profile.user.full_name,
                "last_updated": "2026-07-05T00:00:00Z",
            }
        ]

    @classmethod
    def get_case(cls, user, case_id):
        for case in cls.list_cases(user):
            if str(case["id"]) == str(case_id):
                return case
        return None
