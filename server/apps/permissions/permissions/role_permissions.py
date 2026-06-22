from apps.users.choices import UserRole


class RolePermissions:

    ADMIN = UserRole.ADMIN
    STAFF = UserRole.STAFF
    CLIENT = UserRole.CLIENT
    PORTAL_CLIENT = UserRole.PORTAL_CLIENT

    STAFF_ROLES = [
        STAFF,
    ]