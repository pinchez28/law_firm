from django.db import models


class PartnershipClient(models.Model):

    client = models.OneToOneField(
        "clients.Client",
        on_delete=models.CASCADE,
        related_name="partnership_profile"
    )

    partnership_name = models.CharField(max_length=255)

    registration_number = models.CharField(max_length=100, null=True, blank=True)
    tax_pin = models.CharField(max_length=100, null=True, blank=True)

    formation_date = models.DateField(null=True, blank=True)

    business_address = models.TextField(null=True, blank=True)

    partner_count = models.PositiveIntegerField(default=0)

    managing_partner_name = models.CharField(max_length=255, null=True, blank=True)
    managing_partner_contact = models.CharField(max_length=30, null=True, blank=True)

    agreement_type = models.CharField(max_length=100, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.partnership_name