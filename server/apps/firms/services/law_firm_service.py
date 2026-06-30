from datetime import date

from django.db import transaction

from apps.common.choices import FirmRole, UserRole
from apps.firms.models import LawFirm, LawFirmMember
from apps.staff.models.staff import Staff


class LawFirmService:

    @staticmethod
    @transaction.atomic
    def create_firm(*, validated_data, owner):
        """
        Creates a law firm and fully initializes the owner:
        - assigns firm
        - creates membership
        - creates staff profile
        """

        # -------------------------------------------------
        # 1. Create Law Firm
        # -------------------------------------------------
        firm = LawFirm.objects.create(
            name=validated_data["name"],
            registration_number=validated_data.get("registration_number", ""),
            email=validated_data.get("email", ""),
            phone_number=validated_data.get("phone_number", ""),
            address=validated_data.get("address", ""),
            owner=owner,
        )

        # -------------------------------------------------
        # 2. Ensure owner has correct system role
        # -------------------------------------------------
        if owner.role == UserRole.PORTAL_CLIENT:
            owner.role = UserRole.ADMIN
            owner.save(update_fields=["role"])

        # -------------------------------------------------
        # 3. Create firm membership (idempotent)
        # -------------------------------------------------
        LawFirmMember.objects.get_or_create(
            firm=firm,
            user=owner,
            defaults={
                "role": FirmRole.MANAGING_PARTNER,
                "created_by": owner,
                "is_active": True,
            },
        )

        # -------------------------------------------------
        # 4. Create staff profile (idempotent)
        # -------------------------------------------------
        Staff.objects.get_or_create(
            user=owner,
            law_firm=firm,
            defaults={
                "staff_number": "ADM001",  # TODO: replace with generator later
                "firm_role": FirmRole.MANAGING_PARTNER,
                "job_title": "Managing Partner",
                "date_hired": date.today(),
            },
        )

        return firm