import uuid

from django.db import models

from apps.common.models.timestamped_model import TimestampedModel
from apps.common.choices import (
    EmploymentStatus,
    EmploymentType,
    FirmRole,
)


class Staff(TimestampedModel):
    """
    Represents an employee of a law firm.

    Authentication and personal identity are stored in User.
    Staff stores employment information within a specific law firm.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    user = models.OneToOneField(
        "users.User",
        on_delete=models.CASCADE,
        related_name="staff_profile",
    )

    law_firm = models.ForeignKey(
        "firms.LawFirm",
        on_delete=models.CASCADE,
        related_name="staff_members",
    )

    staff_number = models.CharField(
        max_length=30,
    )

    employee_number = models.CharField(
        max_length=30,
        blank=True,
        null=True,
    )

    firm_role = models.CharField(
        max_length=40,
        choices=FirmRole.choices,
    )

    # department = models.ForeignKey(
    #     # "firms.Department",
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     blank=True,
    #     # related_name="staff_members",
    # )

    department = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    job_title = models.CharField(
        max_length=100,
    )

    work_email = models.EmailField(
        unique=True,
        blank=True,
        null=True,
    )

    work_phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
    )

    office_location = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    reports_to = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="subordinates",
    )

    employment_type = models.CharField(
        max_length=20,
        choices=EmploymentType.choices,
        default=EmploymentType.PERMANENT,
    )

    employment_status = models.CharField(
        max_length=20,
        choices=EmploymentStatus.choices,
        default=EmploymentStatus.ACTIVE,
    )

    date_hired = models.DateField()

    probation_end_date = models.DateField(
        blank=True,
        null=True,
    )

    date_terminated = models.DateField(
        blank=True,
        null=True,
    )

    termination_reason = models.TextField(
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        ordering = ["user__first_name", "user__last_name"]
        verbose_name = "Staff Member"
        verbose_name_plural = "Staff Members"
        constraints = [
            models.UniqueConstraint(
                fields=["law_firm", "staff_number"],
                name="unique_staff_number_per_firm",
            ),
            models.UniqueConstraint(
                fields=["law_firm", "employee_number"],
                name="unique_employee_number_per_firm",
                condition=models.Q(employee_number__isnull=False),
            ),
        ]

    def __str__(self):
        return f"{self.user.full_name} - {self.job_title}"