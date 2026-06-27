from rest_framework import serializers

from apps.clients.models import (
    Client,
    ClientAddress,
    ClientContact,
    IndividualClient,
)


class ClientAddressSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = ClientAddress
        fields = "__all__"


class ClientContactSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = ClientContact
        fields = "__all__"


class IndividualProfileSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = IndividualClient
        exclude = ["client"]


class ClientDetailSerializer(
    serializers.ModelSerializer
):

    individual_profile = serializers.SerializerMethodField()

    addresses = ClientAddressSerializer(
        many=True,
        read_only=True,
    )

    contacts = ClientContactSerializer(
        many=True,
        read_only=True,
    )

    cases = serializers.SerializerMethodField()

    class Meta:
        model = Client

        fields = [
            "id",
            "full_name",
            "email",
            "phone_number",
            "national_id",
            "passport_number",
            "kra_pin",
            "date_of_birth",

            "client_type",
            "access_type",
            "lifecycle_status",
            "is_active",

            "created_at",
            "updated_at",

            "individual_profile",
            "addresses",
            "contacts",

            # Future-ready
            "cases",
        ]

    def get_individual_profile(
        self,
        obj,
    ):
        if hasattr(
            obj,
            "individual_profile",
        ):
            return (
                IndividualProfileSerializer(
                    obj.individual_profile
                ).data
            )

        return None

    def get_cases(
        self,
        obj,
    ):
        """
        Placeholder until Cases module exists.
        """
        return []