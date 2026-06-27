# apps/firms/models/firm_member.py

import uuid

from django.db import models

from apps.common.models.timestamped_model import TimestampedModel


class FirmMember(TimestampedModel):

    class Role(models.TextChoices):
        OWNER = "OWNER", "Owner"
        LAWYER = "LAWYER", "Lawyer"
        SECRETARY = "SECRETARY", "Secretary"
        ACCOUNTANT = "ACCOUNTANT", "Accountant"
        PARALEGAL = "PARALEGAL", "Paralegal"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    firm = models.ForeignKey(
        "firms.LawFirm",
        on_delete=models.CASCADE,
        related_name="members",
    )

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="firm_memberships",
    )

    role = models.CharField(
        max_length=30,
        choices=Role.choices,
    )

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        db_table = "firm_members"

    def __str__(self):
        return f"{self.user.full_name} - {self.role}"