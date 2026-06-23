from django.db import models

from apps.common.models.timestamped_model import TimestampedModel
from .client import Client


class EstateClient(TimestampedModel):

    client = models.OneToOneField(
        Client,
        on_delete=models.CASCADE,
        related_name="estate_details",
        primary_key=True,
    )

    estate_name = models.CharField(
        max_length=255,
    )

    executor_name = models.CharField(
        max_length=255,
    )

    class Meta:
        db_table = "estate_clients"

    def __str__(self):
        return self.estate_name