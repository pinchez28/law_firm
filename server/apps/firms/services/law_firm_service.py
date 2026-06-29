from django.db import transaction

from apps.firms.models import LawFirm, LawFirmMember
from apps.users.choices import UserRole, FirmRole


class LawFirmService:

    @staticmethod
    @transaction.atomic
    def create_firm(*, validated_data, owner):

        firm = LawFirm.objects.create(
            name=validated_data["name"],
            registration_number=validated_data.get("registration_number", ""),
            email=validated_data.get("email", ""),
            phone_number=validated_data.get("phone_number", ""),
            address=validated_data.get("address", ""),
            owner=owner,
        )

        # Ensure owner system role is ADMIN or STAFF (your choice)
        if owner.role == UserRole.PORTAL_CLIENT:
            owner.role = UserRole.ADMIN
            owner.save(update_fields=["role"])

        # Create membership (THIS is what matters for firm access)
        LawFirmMember.objects.create(
            firm=firm,
            user=owner,
            role=FirmRole.LAWYER,
            created_by=owner,
            is_active=True,
        )

        # Ensure user has firm_role in User model (optional but consistent)
        owner.firm_role = FirmRole.LAWYER
        owner.save(update_fields=["firm_role"])

        return firm