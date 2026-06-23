from django.db import models


class ClientAddress(models.Model):

    class AddressType(models.TextChoices):
        HOME = "HOME", "Home"
        WORK = "WORK", "Work"
        POSTAL = "POSTAL", "Postal"
        REGISTERED = "REGISTERED", "Registered"
        OTHER = "OTHER", "Other"

    client = models.ForeignKey(
        "clients.Client",
        on_delete=models.CASCADE,
        related_name="addresses"
    )

    address_type = models.CharField(
        max_length=20,
        choices=AddressType.choices
    )

    country = models.CharField(max_length=100)
    county = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    street = models.CharField(max_length=255, null=True, blank=True)

    postal_code = models.CharField(max_length=50, null=True, blank=True)

    full_address = models.TextField()

    is_primary = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.client.full_name} - {self.address_type}"