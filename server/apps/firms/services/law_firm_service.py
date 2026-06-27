from django.db import transaction
from rest_framework.exceptions import ValidationError

from apps.firms.models import LawFirm


class LawFirmService:

    @staticmethod
    @transaction.atomic
    def create_firm(
        *,
        validated_data,
        owner,
    ):

        if LawFirm.objects.exists():
            raise ValidationError(
                {
                    "message": "A law firm has already been registered in this system."
                }
            )

        firm = LawFirm.objects.create(
            owner=owner,
            name=validated_data["name"],
            registration_number=validated_data.get(
                "registration_number",
                "",
            ),
            email=validated_data.get(
                "email",
                "",
            ),
            phone_number=validated_data.get(
                "phone_number",
                "",
            ),
            address=validated_data.get(
                "address",
                "",
            ),
        )

        return firm