from django.db import models


class CompanyClient(models.Model):

    client = models.OneToOneField(
        "clients.Client",
        on_delete=models.CASCADE,
        related_name="company_profile"
    )

    # ----------------------------------
    # Company Identity
    # ----------------------------------
    company_name = models.CharField(
        max_length=255
    )

    registration_number = models.CharField(
        max_length=100
    )

    tax_pin = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    incorporation_date = models.DateField(
        null=True,
        blank=True
    )

    country_of_incorporation = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    industry = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    company_status = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )

    director_count = models.PositiveIntegerField(
        default=0
    )

    # ----------------------------------
    # Business Address Information
    # ----------------------------------
    business_address = models.TextField(
        null=True,
        blank=True
    )

    postal_address = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    # ----------------------------------
    # Primary Contact Person
    # ----------------------------------
    primary_contact_person = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    primary_contact_email = models.EmailField(
        null=True,
        blank=True
    )

    primary_contact_phone = models.CharField(
        max_length=30,
        null=True,
        blank=True
    )

    # ----------------------------------
    # Audit Fields
    # ----------------------------------
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        db_table = "company_clients"
        verbose_name = "Company Client"
        verbose_name_plural = "Company Clients"

    def __str__(self):
        return self.company_name