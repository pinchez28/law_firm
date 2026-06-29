from django.db import models

class UserRole:
    ADMIN = "ADMIN"
    STAFF = "STAFF"
    OFFICIAL_CLIENT = "OFFICIAL_CLIENT"
    PORTAL_CLIENT = "PORTAL_CLIENT"


USER_ROLE_CHOICES = [
    (UserRole.ADMIN, "Admin"),
    (UserRole.STAFF, "Staff"),
    (UserRole.OFFICIAL_CLIENT, "Official Client"),
    (UserRole.PORTAL_CLIENT, "Portal Client"),
]

class StaffRole(models.TextChoices):
    LAWYER = "LAWYER", "Lawyer"
    SECRETARY = "SECRETARY", "Secretary"
    IT = "IT", "IT Support"
    ACCOUNTANT = "ACCOUNTANT", "Accountant"
    HR = "HR", "Human Resource"
    OFFICE_ASSISTANT = "OFFICE_ASSISTANT", "Office Assistant" 


class FirmRole(models.TextChoices):
    LAWYER = "LAWYER"
    SECRETARY = "SECRETARY"
    IT = "IT"
    ACCOUNTANT = "ACCOUNTANT"
    HR = "HR"
    OFFICE_ASSISTANT = "OFFICE_ASSISTANT"
    OFFICIAL_CLIENT = "OFFICIAL_CLIENT"


FIRM_ROLE_CHOICES = [
    (FirmRole.LAWYER, "Lawyer"),
    (FirmRole.SECRETARY, "Secretary"),
    (FirmRole.IT, "IT"),
    (FirmRole.ACCOUNTANT, "Accountant"),
    (FirmRole.HR, "Human Resource"),
    (FirmRole.OFFICE_ASSISTANT, "Office Assistant"),
    (FirmRole.OFFICIAL_CLIENT, "Official Client"),
]