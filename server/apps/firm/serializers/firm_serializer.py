from rest_framework import serializers

from apps.firm.models import LawFirm


class LawFirmSerializer(serializers.ModelSerializer):
    owner_email = serializers.CharField(source="owner.email", read_only=True)
    owner_name = serializers.CharField(source="owner.full_name", read_only=True)

    class Meta:
        model = LawFirm
        fields = [
            "id",
            "name",
            "registration_number",
            "kra_pin",
            "email",
            "phone_number",
            "website",
            "physical_address",
            "postal_address",
            "description",
            "logo",
            "is_active",
            "owner_email",
            "owner_name",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "registration_number",
            "owner_email",
            "owner_name",
            "created_at",
        ]