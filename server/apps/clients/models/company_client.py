from django.db import models

from apps.common.models.timestamped_model import TimestampedModel
from .client import Client


class CompanyClient(TimestampedModel):

    client = models.OneToOneField(
        Client,
        on_delete=models.CASCADE,
        related_name="company_details",
        primary_key=True,
    )

    company_name = models.CharField(
        max_length=255,
    )

    registration_number = models.CharField(
        max_length=100,
        unique=True,
    )

    tax_number = models.CharField(
        max_length=100,
        blank=True,
    )

    class Meta:
        db_table = "company_clients"

    def __str__(self):
        return self.company_name