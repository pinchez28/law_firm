from datetime import date

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from apps.cases.models import Case
from apps.clients.models import Client
from apps.common.choices import UserRole
from apps.firm.models import LawFirm
from apps.staff.models import Lawyer, Secretary, SecretaryPermissionGrant, SecretaryPermission
from apps.users.models import User


class CaseApiTests(TestCase):
    def setUp(self):
        self.client_api = APIClient()
        self.admin = User.objects.create_user(
            email="case-admin@example.com",
            password="strong-pass123",
            first_name="Case",
            last_name="Admin",
            phone_number="+254744000001",
            national_id_number="744000001",
            role=UserRole.ADMIN,
        )
        self.firm = LawFirm.objects.create(
            name="Case Firm",
            registration_number="CASE-FIRM-001",
            owner=self.admin,
        )
        self.client = Client.objects.create(
            firm=self.firm,
            created_by=self.admin,
            full_name="Mary Wanjiku",
            email="mary@example.com",
            phone_number="+254744000002",
            national_id="744000002",
            client_type=Client.ClientType.INDIVIDUAL,
            lifecycle_status=Client.LifecycleStatus.PROSPECT,
        )
        lawyer_user = User.objects.create_user(
            email="case-lawyer@example.com",
            password="strong-pass123",
            first_name="Lawyer",
            last_name="One",
            phone_number="+254744000003",
            national_id_number="744000003",
            role=UserRole.STAFF,
        )
        self.lawyer = Lawyer.objects.create(
            user=lawyer_user,
            law_firm=self.firm,
            staff_number="LAW-CASE-001",
            admission_number="ADV-CASE-001",
            date_hired=date(2026, 7, 7),
        )
        secretary_user = User.objects.create_user(
            email="case-secretary@example.com",
            password="strong-pass123",
            first_name="Secretary",
            last_name="One",
            phone_number="+254744000004",
            national_id_number="744000004",
            role=UserRole.STAFF,
        )
        self.secretary = Secretary.objects.create(
            user=secretary_user,
            law_firm=self.firm,
            staff_number="SEC-CASE-001",
            date_hired=date(2026, 7, 7),
        )
        SecretaryPermissionGrant.objects.create(
            secretary=self.secretary,
            code=SecretaryPermission.MANAGE_CASES,
            granted_by=self.admin,
        )
        self.client_api.force_authenticate(user=self.admin)

    def payload(self):
        return {
            "client_id": str(self.client.id),
            "assigned_lawyer_membership_id": str(self.lawyer.id),
            "assigned_secretary_membership_id": str(self.secretary.id),
            "case_number": "CASE-2026-001",
            "title": "Land Boundary Dispute",
            "description": "Boundary dispute between neighbours.",
            "case_type": Case.CaseType.LAND,
            "court_type": Case.CourtType.ENVIRONMENT_LAND,
            "priority": Case.Priority.HIGH,
            "filing_date": "2026-07-07",
            "court_name": "ELC Nairobi",
            "court_location": "Nairobi",
            "defendant": "John Doe",
        }

    def test_admin_creates_case_for_existing_client_and_promotes_client(self):
        response = self.client_api.post(reverse("case-create"), self.payload(), format="json")

        self.assertEqual(response.status_code, 201, response.data)
        created = Case.objects.get(case_number="CASE-2026-001")
        self.assertEqual(created.client, self.client)
        self.assertEqual(created.assigned_lawyer, self.lawyer)
        self.assertEqual(created.assigned_secretary, self.secretary)

        self.client.refresh_from_db()
        self.assertEqual(
            self.client.lifecycle_status,
            Client.LifecycleStatus.OFFICIAL_CLIENT,
        )

    def test_case_creation_rejects_missing_client(self):
        payload = self.payload()
        payload["client_id"] = "123e4567-e89b-12d3-a456-426614174000"

        response = self.client_api.post(reverse("case-create"), payload, format="json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Case.objects.count(), 0)

    def test_lawyer_only_sees_assigned_cases(self):
        response = self.client_api.post(reverse("case-create"), self.payload(), format="json")
        self.assertEqual(response.status_code, 201, response.data)

        self.client_api.force_authenticate(user=self.lawyer.user)
        list_response = self.client_api.get(reverse("lawyer-cases"))

        self.assertEqual(list_response.status_code, 200)
        self.assertEqual(len(list_response.data["cases"]), 1)
        self.assertEqual(list_response.data["cases"][0]["title"], "Land Boundary Dispute")

    def test_secretary_only_sees_assigned_cases_when_permitted(self):
        response = self.client_api.post(reverse("case-create"), self.payload(), format="json")
        self.assertEqual(response.status_code, 201, response.data)

        self.client_api.force_authenticate(user=self.secretary.user)
        list_response = self.client_api.get(reverse("secretary-cases"))

        self.assertEqual(list_response.status_code, 200)
        self.assertEqual(len(list_response.data["cases"]), 1)
