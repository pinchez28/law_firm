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
    MANAGING_PARTNER = "MANAGING_PARTNER", "Managing Partner"
    SENIOR_PARTNER = "SENIOR_PARTNER", "Senior Partner"
    PARTNER = "PARTNER", "Partner"

    ASSOCIATE = "ASSOCIATE", "Associate"
    SENIOR_ASSOCIATE = "SENIOR_ASSOCIATE", "Senior Associate"

    PUPIL = "PUPIL", "Pupil"
    LEGAL_INTERN = "LEGAL_INTERN", "Legal Intern"

    SECRETARY = "SECRETARY", "Secretary"
    PARALEGAL = "PARALEGAL", "Paralegal"
    LEGAL_CLERK = "LEGAL_CLERK", "Legal Clerk"

    ACCOUNTANT = "ACCOUNTANT", "Accountant"
    HR = "HR", "Human Resource"
    IT = "IT", "IT Support"
    OFFICE_ADMINISTRATOR = "OFFICE_ADMINISTRATOR", "Office Administrator"
    OFFICE_ASSISTANT = "OFFICE_ASSISTANT", "Office Assistant"
    RECEPTIONIST = "RECEPTIONIST", "Receptionist"
    MESSENGER = "MESSENGER", "Messenger"


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