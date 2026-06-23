import uuid

from django.conf import settings
from django.utils import timezone
from django.db import models

from apps.common.models.timestamped_model import TimestampedModel


class ClientType(models.TextChoices):
    INDIVIDUAL = "INDIVIDUAL", "Individual"
    COMPANY = "COMPANY", "Company"
    PARTNERSHIP = "PARTNERSHIP", "Partnership"
    NGO = "NGO", "NGO"
    TRUST = "TRUST", "Trust"
    ESTATE = "ESTATE", "Estate"
    GOVERNMENT = "GOVERNMENT", "Government"
    OTHER = "OTHER", "Other"


class ClientOnboardingType(models.TextChoices):
    PUBLIC_REGISTRATION = "PUBLIC_REGISTRATION", "Public Registration"
    FIRM_CREATED = "FIRM_CREATED", "Firm Created"
    ASSISTED = "ASSISTED", "Assisted Client"


class Client(TimestampedModel):
    """
    Core legal client entity.

    A client may be:
    - Individual
    - Company
    - Estate
    - Trust
    - NGO
    - Partnership
    - Government Entity

    A client may or may not have a login account.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="client",
    )

    client_number = models.CharField(
        max_length=30,
        unique=True,
        editable=False,
    )

    client_type = models.CharField(
        max_length=30,
        choices=ClientType.choices,
    )

    onboarding_type = models.CharField(
        max_length=30,
        choices=ClientOnboardingType.choices,
    )

    portal_enabled = models.BooleanField(
        default=False,
    )

    is_active = models.BooleanField(
        default=True,
    )

    notes = models.TextField(
        blank=True,
    )

    class Meta:
        db_table = "clients"
        ordering = ["-created_at"]

    @property
    def display_name(self):
        """
        Human-readable client name.
        """

        if (
            self.client_type == ClientType.INDIVIDUAL
            and hasattr(self, "individual_details")
        ):
            return (
                f"{self.individual_details.first_name} "
                f"{self.individual_details.last_name}"
            )

        if (
            self.client_type == ClientType.COMPANY
            and hasattr(self, "company_details")
        ):
            return self.company_details.company_name

        if (
            self.client_type == ClientType.ESTATE
            and hasattr(self, "estate_details")
        ):
            return self.estate_details.estate_name

        if (
            self.client_type == ClientType.TRUST
            and hasattr(self, "trust_details")
        ):
            return self.trust_details.trust_name

        return self.client_number

    def save(self, *args, **kwargs):
        """
        Auto-generate client number.
        """

        if not self.client_number:

            year = timezone.now().year

            last_client = (
                Client.objects
                .order_by("-created_at")
                .first()
            )

            if (
                last_client
                and last_client.client_number
            ):
                try:
                    last_number = int(
                        last_client.client_number.split("-")[-1]
                    )
                except (ValueError, IndexError):
                    last_number = 0
            else:
                last_number = 0

            next_number = last_number + 1

            self.client_number = (
                f"CLI-{year}-{next_number:06d}"
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return self.display_name