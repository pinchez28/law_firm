from rest_framework import serializers

from apps.firms.models import LawFirm


class LawFirmSerializer(serializers.ModelSerializer):

    owner_name = serializers.CharField(
        source="owner.full_name",
        read_only=True,
    )

    class Meta:
        model = LawFirm

        fields = [
            "id",
            "name",
            "registration_number",
            "email",
            "phone_number",
            "address",
            "owner",
            "owner_name",
            "is_active",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "owner",
            "owner_name",
            "created_at",
            "updated_at",
        ]