class ClientCaseService:
    @staticmethod
    def list_cases(client):
        return [
            {
                "id": "case-001",
                "title": "Estate administration",
                "status": "OPEN",
                "last_updated": "2026-07-05",
            }
        ]
