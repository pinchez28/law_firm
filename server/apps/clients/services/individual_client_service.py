from django.db import transaction

from apps.clients.models import (
    Client,
    IndividualClient,
    ClientAddress,
    ClientContact,
    ContactType,
)


class IndividualClientService:

    @staticmethod
    @transaction.atomic
    def create_client(
        *,
        validated_data,
        user,
    ):
        """
        Creates:
        1. Client
        2. IndividualClient
        3. Primary Address
        4. Primary Contact
        """

        # ----------------------------------
        # Core Client
        # ----------------------------------

        client = Client.objects.create(
            firm=getattr(user, "firm", None),
            created_by=user,
            full_name=validated_data["full_name"],
            email=validated_data.get("email"),
            phone_number=validated_data["phone_number"],
            client_type=Client.ClientType.INDIVIDUAL,
            onboarding_type=validated_data["onboarding_type"],
            portal_enabled=validated_data["portal_enabled"],
            national_id=validated_data.get("national_id"),
            passport_number=validated_data.get("passport_number"),
            kra_pin=validated_data.get("kra_pin"),
            date_of_birth=validated_data.get("date_of_birth"),
        )

        # ----------------------------------
        # Individual Profile
        # ----------------------------------

        IndividualClient.objects.create(
            client=client,
            gender=validated_data.get("gender"),
            occupation=validated_data.get("occupation"),
            marital_status=validated_data.get("marital_status"),
            next_of_kin_name=validated_data.get(
                "next_of_kin_name"
            ),
            next_of_kin_phone=validated_data.get(
                "next_of_kin_phone"
            ),
            next_of_kin_relationship=validated_data.get(
                "next_of_kin_relationship"
            ),
            emergency_contact_name=validated_data.get(
                "emergency_contact_name"
            ),
            emergency_contact_phone=validated_data.get(
                "emergency_contact_phone"
            ),
        )

        # ----------------------------------
        # Primary Contact
        # ----------------------------------

        ClientContact.objects.create(
            client=client,
            contact_type=ContactType.PRIMARY,
            full_name=client.full_name,
            email=client.email or "",
            phone_number=client.phone_number,
            is_primary=True,
        )

        # ----------------------------------
        # Primary Address
        # ----------------------------------

        ClientAddress.objects.create(
            client=client,
            address_type=ClientAddress.AddressType.HOME,
            country=validated_data["country"],
            county=validated_data.get("county"),
            city=validated_data.get("city"),
            street=validated_data.get("street"),
            postal_code=validated_data.get("postal_code"),
            full_address=validated_data["full_address"],
            is_primary=True,
        )

        return client