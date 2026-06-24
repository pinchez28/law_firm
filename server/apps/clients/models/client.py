import uuid

from django.db import models


class Client(models.Model):

    class ClientType(models.TextChoices):
        INDIVIDUAL = "INDIVIDUAL", "Individual"
        COMPANY = "COMPANY", "Company"
        PARTNERSHIP = "PARTNERSHIP", "Partnership"
        NGO = "NGO", "NGO"
        TRUST = "TRUST", "Trust"
        ESTATE = "ESTATE", "Estate"
        GOVERNMENT = "GOVERNMENT", "Government"
        OTHER = "OTHER", "Other"

    class OnboardingType(models.TextChoices):
        PORTAL = "PORTAL", "Portal Created"
        ASSISTED = "ASSISTED", "Assisted"

    class LifecycleStatus(models.TextChoices):
        PORTAL_PENDING = "PORTAL_PENDING", "Portal Pending"
        OFFICIAL_CLIENT = "OFFICIAL_CLIENT", "Official Client"
        ARCHIVED = "ARCHIVED", "Archived"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    firm = models.ForeignKey(
        "firms.LawFirm",
        on_delete=models.CASCADE,
        related_name="clients",
        null=True,
        blank=True
    )

    created_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_clients"
    )

    user = models.OneToOneField(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="client_profile"
    )

    # Core Client Information

    full_name = models.CharField(
        max_length=255
    )

    email = models.EmailField(
        null=True,
        blank=True
    )

    phone_number = models.CharField(
        max_length=30
    )

    # Client Classification

    client_type = models.CharField(
        max_length=30,
        choices=ClientType.choices
    )

    onboarding_type = models.CharField(
        max_length=20,
        choices=OnboardingType.choices
    )

    portal_enabled = models.BooleanField(
        default=False
    )

    # Identification Information

    national_id = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )

    passport_number = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )

    kra_pin = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True
    )

    # Client Lifecycle

    lifecycle_status = models.CharField(
        max_length=30,
        choices=LifecycleStatus.choices,
        default=LifecycleStatus.PORTAL_PENDING
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        db_table = "clients"

    def __str__(self):
        return self.full_name