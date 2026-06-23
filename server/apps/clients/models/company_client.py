from django.db import models


class CompanyClient(models.Model):

    client = models.OneToOneField(
        "clients.Client",
        on_delete=models.CASCADE,
        related_name="company_profile"
    )

    company_name = models.CharField(max_length=255)

    registration_number = models.CharField(max_length=100)
    tax_pin = models.CharField(max_length=100, null=True, blank=True)

    incorporation_date = models.DateField(null=True, blank=True)
    country_of_incorporation = models.CharField(max_length=100, null=True, blank=True)

    industry = models.CharField(max_length=100, null=True, blank=True)

    business_address = models.TextField(null=True, blank=True)
    postal_address = models.CharField(max_length=255, null=True, blank=True)

    primary_contact_person = models.CharField(max_length=255, null=True, blank=True)
    primary_contact_email = models.EmailField(null=True, blank=True)
    primary_contact_phone = models.CharField(max_length=30, null=True, blank=True)

    director_count = models.PositiveIntegerField(default=0)

    company_status = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_name