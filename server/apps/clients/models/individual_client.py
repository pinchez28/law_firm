from django.db import models

from apps.common.models.timestamped_model import TimestampedModel
from .client import Client


class IndividualClient(TimestampedModel):
    """
    Individual legal person.
    """

    client = models.OneToOneField(
        Client,
        on_delete=models.CASCADE,
        related_name="individual_details",
    )

    first_name = models.CharField(
        max_length=100,
    )

    middle_name = models.CharField(
        max_length=100,
        blank=True,
    )

    last_name = models.CharField(
        max_length=100,
    )

    national_id_number = models.CharField(
        max_length=20,
        unique=True,
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "individual_clients"

    def __str__(self):
        return (
            f"{self.first_name} "
            f"{self.last_name}"
        )