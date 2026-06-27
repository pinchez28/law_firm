import re
from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import transaction

from apps.clients.models.client import Client
from apps.clients.models.client_address import ClientAddress
from apps.clients.models.client_contact import ClientContact, ContactType
from apps.clients.models.company_client import CompanyClient
from apps.users.choices import UserRole

User = get_user_model()


def generate_temp_password(company_name: str) -> str:
    """
    Generates a memorable temporary password.

    Example:
    ABC Holdings Ltd -> ABCHO2026
    Microsoft Kenya -> MICRO2026
    IBM -> IBMXX2026
    """

    cleaned = re.sub(r"[^A-Za-z0-9]", "", company_name)

    prefix = cleaned[:5].upper().ljust(5, "X")

    return f"{prefix}{datetime.now().year}"


class CompanyClientService:

    @staticmethod
    @transaction.atomic
    def create_client(*, validated_data, user):

        company_name = validated_data["company_name"]

        temp_password = generate_temp_password(company_name)

        # ----------------------------------------
        # Split contact name
        # ----------------------------------------

        full_name = validated_data["contact_full_name"].strip()
        name_parts = full_name.split(maxsplit=1)

        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ""

        # ----------------------------------------
        # Base Client
        # ----------------------------------------

        client = Client.objects.create(
            firm=user.firm,
            created_by=user,
            full_name=company_name,
            email=validated_data["email"],
            phone_number=validated_data.get("phone_number", ""),
            client_type=Client.ClientType.COMPANY,
            access_type=Client.AccessType.PORTAL_CLIENT,
        )

        # ----------------------------------------
        # Company Profile
        # ----------------------------------------

        company = CompanyClient.objects.create(
            client=client,
            company_name=company_name,
            registration_number=validated_data["registration_number"],
            incorporation_date=validated_data.get("incorporation_date"),
            country_of_incorporation=validated_data.get(
                "country_of_incorporation",
                "",
            ),
            industry=validated_data.get("industry", ""),
            company_status=validated_data.get(
                "company_status",
                CompanyClient.CompanyStatus.ACTIVE,
            ),
            director_count=validated_data.get("director_count", 0),
        )

        # ----------------------------------------
        # Portal User
        # ----------------------------------------

        portal_user = User.objects.create_user(
            email=validated_data["contact_email"],
            password=temp_password,
            first_name=first_name,
            last_name=last_name,
            phone_number=validated_data["contact_phone_number"],
            national_id_number=validated_data[
                "contact_national_id_number"
            ],
            role=UserRole.PORTAL_CLIENT,
            must_change_password=True,
        )

        company.user = portal_user
        company.save(update_fields=["user"])

        # ----------------------------------------
        # Registered Address
        # ----------------------------------------

        ClientAddress.objects.create(
            client=client,
            address_type=ClientAddress.AddressType.REGISTERED,
            country=validated_data["country"],
            county=validated_data.get("county", ""),
            city=validated_data.get("city", ""),
            street=validated_data.get("street", ""),
            postal_code=validated_data.get("postal_code", ""),
            full_address=validated_data["full_address"],
            is_primary=True,
        )

        # ----------------------------------------
        # Primary Contact
        # ----------------------------------------

        ClientContact.objects.create(
            client=client,
            contact_type=ContactType.PRIMARY,
            full_name=validated_data["contact_full_name"],
            role_or_designation=validated_data.get(
                "contact_role_or_designation",
                "Authorized Representative",
            ),
            email=validated_data["contact_email"],
            phone_number=validated_data["contact_phone_number"],
            is_primary=True,
        )

        # ----------------------------------------
        # Response
        # ----------------------------------------

        return {
            "client": client,
            "company": company,
            "portal_user": portal_user,
            "temp_password": temp_password,
        }