from django.db import transaction

from apps.clients.models import (
    Client,
    CompanyClient,
    ClientAddress,
    ClientContact,
    ContactType,
)


class CompanyClientService:

    @staticmethod
    @transaction.atomic
    def create_client(*, validated_data, user):

        # ----------------------------------
        # 1. Base Client
        # ----------------------------------
        client = Client.objects.create(
            firm=getattr(user, "firm", None),
            created_by=user,
            full_name=validated_data.get("company_name"),
            email=validated_data.get("primary_contact_email"),
            phone_number=validated_data.get("primary_contact_phone", ""),
            client_type=Client.ClientType.COMPANY,
            onboarding_type=validated_data["onboarding_type"],
            portal_enabled=validated_data.get("portal_enabled", False),
            kra_pin=validated_data.get("tax_pin"),
        )

        # ----------------------------------
        # 2. Company Profile
        # ----------------------------------
        CompanyClient.objects.create(
            client=client,
            company_name=validated_data["company_name"],
            registration_number=validated_data["registration_number"],
            tax_pin=validated_data.get("tax_pin"),
            incorporation_date=validated_data.get("incorporation_date"),
            country_of_incorporation=validated_data.get("country_of_incorporation"),
            industry=validated_data.get("industry"),
            business_address=validated_data.get("business_address"),
            postal_address=validated_data.get("postal_address"),
            primary_contact_person=validated_data.get("primary_contact_person"),
            primary_contact_email=validated_data.get("primary_contact_email"),
            primary_contact_phone=validated_data.get("primary_contact_phone"),
            director_count=validated_data.get("director_count", 0),
            company_status=validated_data.get("company_status"),
        )

        # ----------------------------------
        # 3. Primary Contact
        # ----------------------------------
        ClientContact.objects.create(
            client=client,
            contact_type=ContactType.PRIMARY,
            full_name=validated_data.get("primary_contact_person")
                       or validated_data["company_name"],
            email=validated_data.get("primary_contact_email", ""),
            phone_number=validated_data.get("primary_contact_phone", ""),
            is_primary=True,
        )

        # ----------------------------------
        # 4. Address
        # ----------------------------------
        ClientAddress.objects.create(
            client=client,
            address_type=ClientAddress.AddressType.OFFICE,
            country=validated_data["country"],
            county=validated_data.get("county", ""),
            city=validated_data.get("city", ""),
            street=validated_data.get("street", ""),
            postal_code=validated_data.get("postal_code", ""),
            full_address=validated_data["full_address"],
            is_primary=True,
        )

        return client