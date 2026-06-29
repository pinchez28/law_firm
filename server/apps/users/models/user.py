import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from apps.common.models.timestamped_model import TimestampedModel
from apps.users.choices import (
    UserRole,
    FirmRole,
    USER_ROLE_CHOICES,
    FIRM_ROLE_CHOICES,
)
from apps.users.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin, TimestampedModel):
    """
    System identity model.

    A User represents anyone who can authenticate into the system.

    System Roles:
        - ADMIN
        - STAFF
        - OFFICIAL_CLIENT
        - PORTAL_CLIENT

    Firm Roles:
        - LAWYER
        - SECRETARY
        - IT
        - ACCOUNTANT
        - HR
        - OFFICE_ASSISTANT
        - OFFICIAL_CLIENT
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    email = models.EmailField(
        unique=True,
    )

    first_name = models.CharField(
        max_length=100,
    )

    last_name = models.CharField(
        max_length=100,
    )

    national_id_number = models.CharField(
        max_length=20,
        unique=True,
    )

    phone_number = models.CharField(
        max_length=20,
        unique=True,
    )

    # Authentication / Authorization Role
    role = models.CharField(
        max_length=30,
        choices=USER_ROLE_CHOICES,
        default=UserRole.PORTAL_CLIENT,
    )

    # Profession within the firm
    firm_role = models.CharField(
        max_length=30,
        choices=FIRM_ROLE_CHOICES,
        null=True,
        blank=True,
    )

    firm = models.ForeignKey(
        "firms.LawFirm",
        on_delete=models.CASCADE,
        related_name="users",
        null=True,
        blank=True,
    )

    must_change_password = models.BooleanField(
        default=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    is_staff = models.BooleanField(
        default=False,
    )

    objects = UserManager()

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
        "phone_number",
        "national_id_number",
    ]

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    # ---------- System Roles ----------

    @property
    def is_admin(self):
        return self.role == UserRole.ADMIN

    @property
    def is_staff_user(self):
        return self.role == UserRole.STAFF

    @property
    def is_official_client(self):
        return self.role == UserRole.OFFICIAL_CLIENT

    @property
    def is_portal_client(self):
        return self.role == UserRole.PORTAL_CLIENT

    # ---------- Firm Roles ----------

    @property
    def is_lawyer(self):
        return self.firm_role == FirmRole.LAWYER

    @property
    def is_secretary(self):
        return self.firm_role == FirmRole.SECRETARY

    @property
    def is_it(self):
        return self.firm_role == FirmRole.IT

    @property
    def is_accountant(self):
        return self.firm_role == FirmRole.ACCOUNTANT

    @property
    def is_hr(self):
        return self.firm_role == FirmRole.HR

    @property
    def is_office_assistant(self):
        return self.firm_role == FirmRole.OFFICE_ASSISTANT

    def __str__(self):
        return f"{self.full_name} ({self.email})"