from rest_framework import serializers
from apps.clients.models import Client


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client

        fields = (
            "id",
            "client_type",
            "onboarding_type",
            "portal_enabled",
            "lifecycle_status",
            "is_active",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "lifecycle_status",
            "created_at",
            "updated_at",
        )