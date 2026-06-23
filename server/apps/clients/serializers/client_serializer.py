from rest_framework import serializers

from apps.clients.models import Client


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client

        fields = (
            "id",
            "client_number",
            "client_type",
            "onboarding_type",
            "portal_enabled",
            "is_active",
            "notes",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "client_number",
            "created_at",
            "updated_at",
        )