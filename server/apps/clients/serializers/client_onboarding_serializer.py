from rest_framework import serializers
from apps.clients.models import Client


class ClientOnboardingSerializer(serializers.Serializer):

    onboarding_type = serializers.ChoiceField(
        choices=Client.OnboardingType.choices
    )

    client_type = serializers.ChoiceField(
        choices=Client.ClientType.choices
    )

    notes = serializers.CharField(
        required=False,
        allow_blank=True
    )

    def validate(self, attrs):
        onboarding_type = attrs.get("onboarding_type")
        client_type = attrs.get("client_type")

        if onboarding_type == "ASSISTED" and not client_type:
            raise serializers.ValidationError(
                "Client type is required for assisted onboarding"
            )

        return attrs