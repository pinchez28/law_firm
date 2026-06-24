from rest_framework import serializers

from apps.clients.models import Client, IndividualClient


class IndividualClientCreateSerializer(serializers.Serializer):

    # ----------------------------------
    # Client
    # ----------------------------------

    full_name = serializers.CharField(max_length=255)

    email = serializers.EmailField(
        required=False,
        allow_blank=True,
        allow_null=True,
    )

    phone_number = serializers.CharField(max_length=30)

    onboarding_type = serializers.ChoiceField(
        choices=Client.OnboardingType.choices
    )

    portal_enabled = serializers.BooleanField(
        default=False
    )

    national_id = serializers.CharField(
        required=False,
        allow_blank=True,
    )

    passport_number = serializers.CharField(
        required=False,
        allow_blank=True,
    )

    kra_pin = serializers.CharField(
        required=False,
        allow_blank=True,
    )

    date_of_birth = serializers.DateField(
        required=False,
        allow_null=True,
    )

    # ----------------------------------
    # Individual Profile
    # ----------------------------------

    gender = serializers.ChoiceField(
        choices=IndividualClient.Gender.choices,
        required=True,
    )

    occupation = serializers.CharField(
        required=False,
        allow_blank=True,
    )

    marital_status = serializers.ChoiceField(
        choices=IndividualClient.MaritalStatus.choices,
        required=False,
    )

    next_of_kin_name = serializers.CharField(
        required=False,
        allow_blank=True,
    )

    next_of_kin_phone = serializers.CharField(
        required=False,
        allow_blank=True,
    )

    next_of_kin_relationship = serializers.CharField(
        required=False,
        allow_blank=True,
    )

    emergency_contact_name = serializers.CharField(
        required=False,
        allow_blank=True,
    )

    emergency_contact_phone = serializers.CharField(
        required=False,
        allow_blank=True,
    )

    # ----------------------------------
    # Address
    # ----------------------------------

    country = serializers.CharField(max_length=100)

    county = serializers.CharField(
        required=False,
        allow_blank=True,
    )

    city = serializers.CharField(
        required=False,
        allow_blank=True,
    )

    street = serializers.CharField(
        required=False,
        allow_blank=True,
    )

    postal_code = serializers.CharField(
        required=False,
        allow_blank=True,
    )

    full_address = serializers.CharField()

    def validate(self, attrs):

        national_id = attrs.get("national_id")
        passport_number = attrs.get("passport_number")

        if not national_id and not passport_number:
            raise serializers.ValidationError(
                "Either national_id or passport_number is required."
            )

        return attrs