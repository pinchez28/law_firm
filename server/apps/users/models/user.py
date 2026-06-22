import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from apps.common.models.timestamped_model import TimestampedModel
from ..managers import UserManager
from ..choices import USER_ROLE_CHOICES, UserRole


class User(AbstractBaseUser, PermissionsMixin, TimestampedModel):
    """
    System identity model.

    Users are login-capable actors:

    - Admins
    - Staff Members
    - Portal Clients
    - Official Clients

    Specific staff responsibilities such as
    Lawyer and Secretary are modeled in their
    respective business-domain apps.

    Assisted/offline clients without login credentials
    should exist only in the clients app.
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

    role = models.CharField(
        max_length=30,
        choices=USER_ROLE_CHOICES,
        default=UserRole.PORTAL_CLIENT,
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

    def __str__(self):
        return f"{self.full_name} ({self.email})"