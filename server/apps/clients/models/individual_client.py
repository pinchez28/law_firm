from django.db import models


class IndividualClient(models.Model):

    client = models.OneToOneField(
        "clients.Client",
        on_delete=models.CASCADE,
        related_name="individual_profile"
    )

    national_id = models.CharField(max_length=50, null=True, blank=True)
    passport_number = models.CharField(max_length=50, null=True, blank=True)

    kra_pin = models.CharField(max_length=50, null=True, blank=True)

    date_of_birth = models.DateField(null=True, blank=True)

    gender = models.CharField(max_length=20, null=True, blank=True)

    occupation = models.CharField(max_length=255, null=True, blank=True)

    marital_status = models.CharField(max_length=50, null=True, blank=True)

    next_of_kin_name = models.CharField(max_length=255, null=True, blank=True)
    next_of_kin_phone = models.CharField(max_length=30, null=True, blank=True)
    next_of_kin_relationship = models.CharField(max_length=100, null=True, blank=True)

    emergency_contact_name = models.CharField(max_length=255, null=True, blank=True)
    emergency_contact_phone = models.CharField(max_length=30, null=True, blank=True)

    home_address = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Individual: {self.client.full_name}"