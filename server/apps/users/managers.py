from django.contrib.auth.base_user import BaseUserManager

from apps.users.choices import (
    UserRole,
    FirmRole,
)


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """
        Base user creation method.

        Used internally by all other creation methods.
        """

        if not email:
            raise ValueError("Email is required.")

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            **extra_fields,
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_admin(
        self,
        email,
        password=None,
        **extra_fields,
    ):
        """
        Creates a firm administrator.

        Allowed firm roles:
            - LAWYER
            - IT
        """

        firm_role = extra_fields.get("firm_role")

        if firm_role not in (
            FirmRole.LAWYER,
            FirmRole.IT,
        ):
            raise ValueError(
                "An Admin must have a firm role of LAWYER or IT."
            )

        extra_fields["role"] = UserRole.ADMIN
        extra_fields.setdefault("is_staff", True)

        return self.create_user(
            email,
            password,
            **extra_fields,
        )

    def create_staff(
        self,
        email,
        password=None,
        **extra_fields,
    ):
        """
        Creates a staff member.
        """

        allowed_roles = (
            FirmRole.LAWYER,
            FirmRole.SECRETARY,
            FirmRole.IT,
            FirmRole.ACCOUNTANT,
            FirmRole.HR,
            FirmRole.OFFICE_ASSISTANT,
        )

        firm_role = extra_fields.get("firm_role")

        if firm_role not in allowed_roles:
            raise ValueError(
                "Invalid firm role for a staff member."
            )

        extra_fields["role"] = UserRole.STAFF

        return self.create_user(
            email,
            password,
            **extra_fields,
        )

    def create_portal_client(
        self,
        email,
        password=None,
        **extra_fields,
    ):
        """
        Creates a portal client.

        Portal clients are not yet attached
        to a law firm.
        """

        extra_fields["role"] = UserRole.PORTAL_CLIENT
        extra_fields["firm_role"] = None
        extra_fields["firm"] = None

        return self.create_user(
            email,
            password,
            **extra_fields,
        )

    def create_official_client(
        self,
        email,
        password=None,
        **extra_fields,
    ):
        """
        Creates an official client.

        Official clients belong to a law firm.
        """

        if not extra_fields.get("firm"):
            raise ValueError(
                "Official Client must belong to a law firm."
            )

        extra_fields["role"] = UserRole.OFFICIAL_CLIENT
        extra_fields["firm_role"] = FirmRole.OFFICIAL_CLIENT

        return self.create_user(
            email,
            password,
            **extra_fields,
        )

    def create_superuser(
        self,
        email,
        password=None,
        **extra_fields,
    ):
        """
        Django superuser.

        Used only for Django Admin.
        """

        extra_fields.setdefault(
            "is_staff",
            True,
        )

        extra_fields.setdefault(
            "is_superuser",
            True,
        )

        extra_fields.setdefault(
            "role",
            UserRole.ADMIN,
        )

        extra_fields.setdefault(
            "firm_role",
            FirmRole.IT,
        )

        if extra_fields.get("is_staff") is not True:
            raise ValueError(
                "Superuser must have is_staff=True."
            )

        if extra_fields.get("is_superuser") is not True:
            raise ValueError(
                "Superuser must have is_superuser=True."
            )

        return self.create_user(
            email,
            password,
            **extra_fields,
        )