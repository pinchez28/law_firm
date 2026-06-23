from django.db import models

from apps.common.models.timestamped_model import TimestampedModel
from .client import Client


class TrustClient(TimestampedModel):

    client = models.OneToOneField(
        Client,
        on_delete=models.CASCADE,
        related_name="trust_details",
        primary_key=True,
    )

    trust_name = models.CharField(
        max_length=255,
    )

    trust_reference = models.CharField(
        max_length=100,
        blank=True,
    )

    class Meta:
        db_table = "trust_clients"

    def __str__(self):
        return self.trust_name