from django.db import models


# ==========================================================
# System Roles
# ==========================================================

class UserRole(models.TextChoices):
    ADMIN = "ADMIN", "Admin"
    STAFF = "STAFF", "Staff"
    OFFICIAL_CLIENT = "OFFICIAL_CLIENT", "Official Client"
    PORTAL_CLIENT = "PORTAL_CLIENT", "Portal Client"


# ==========================================================
# Law Firm Roles
# ==========================================================

class FirmRole(models.TextChoices):
    # Lawyers
    MANAGING_PARTNER = "MANAGING_PARTNER", "Managing Partner"
    PARTNER = "PARTNER", "Partner"
    ASSOCIATE = "ASSOCIATE", "Associate"
    LEGAL_INTERN = "LEGAL_INTERN", "Legal Intern"

    # Administration
    SECRETARY = "SECRETARY", "Secretary"
    ACCOUNTANT = "ACCOUNTANT", "Accountant"
    HR = "HR", "Human Resource"
    IT = "IT", "IT Support"

    @classmethod
    def lawyer_roles(cls):
        return [
            cls.MANAGING_PARTNER,
            cls.PARTNER,
            cls.ASSOCIATE,
            cls.LEGAL_INTERN,
        ]

    @classmethod
    def staff_roles(cls):
        return [
            cls.SECRETARY,
            cls.ACCOUNTANT,
            cls.HR,
            cls.IT,
        ]
# ==========================================================
# Employment Types
# ==========================================================

class EmploymentType(models.TextChoices):
    PERMANENT = "PERMANENT", "Permanent"
    CONTRACT = "CONTRACT", "Contract"
    PART_TIME = "PART_TIME", "Part Time"
    INTERN = "INTERN", "Intern"
    CONSULTANT = "CONSULTANT", "Consultant"
    TEMPORARY = "TEMPORARY", "Temporary"


# ==========================================================
# Employment Status
# ==========================================================

class EmploymentStatus(models.TextChoices):
    ACTIVE = "ACTIVE", "Active"
    PROBATION = "PROBATION", "Probation"
    ON_LEAVE = "ON_LEAVE", "On Leave"
    SUSPENDED = "SUSPENDED", "Suspended"
    RESIGNED = "RESIGNED", "Resigned"
    TERMINATED = "TERMINATED", "Terminated"
    RETIRED = "RETIRED", "Retired"