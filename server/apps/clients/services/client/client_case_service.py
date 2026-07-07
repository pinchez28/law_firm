class ClientCaseService:
    @staticmethod
    def list_cases(client):
        return [
            {
                "id": "22222222-2222-2222-2222-222222222222",
                "title": "Estate administration",
                "status": "OPEN",
                "last_updated": "2026-07-05",
            }
        ]

    @classmethod
    def get_case(cls, client, case_id):
        for case in cls.list_cases(client):
            if str(case["id"]) == str(case_id):
                return case
        return None
