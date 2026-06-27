import uuid

from django.db import models

from apps.common.models.timestamped_model import TimestampedModel


class LawFirm(TimestampedModel):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        max_length=255,
        unique=True,
    )

    registration_number = models.CharField(
        max_length=100,
        blank=True,
    )

    email = models.EmailField(
        blank=True,
    )

    phone_number = models.CharField(
        max_length=30,
        blank=True,
    )

    address = models.TextField(
        blank=True,
    )

    owner = models.OneToOneField(
        "users.User",
        on_delete=models.CASCADE,
        related_name="owned_firm",
    )

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        db_table = "law_firms"

    def __str__(self):
        return self.name