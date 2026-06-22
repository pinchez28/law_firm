# apps/users/choices.py

class UserRole:
    """
    System-wide user roles.

    ADMIN:
        System administrator with full platform access.

    STAFF:
        Internal law firm personnel.
        Specific staff functions (Lawyer, Secretary, etc.)
        are modeled in their respective apps.

    CLIENT:
        Official client of the law firm.

    PORTAL_CLIENT:
        External user with limited portal access.
        Can later be promoted to CLIENT.
    """

    ADMIN = "ADMIN"
    STAFF = "STAFF"
    CLIENT = "CLIENT"
    PORTAL_CLIENT = "PORTAL_CLIENT"


USER_ROLE_CHOICES = [
    (UserRole.ADMIN, "Admin"),
    (UserRole.STAFF, "Staff"),
    (UserRole.CLIENT, "Client"),
    (UserRole.PORTAL_CLIENT, "Portal Client"),
]