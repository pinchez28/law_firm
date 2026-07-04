from datetime import date
from django.db import transaction

from apps.users.models import User
from apps.firm.models import (
    LawFirm,
    Branch,
    Department,
    PracticeArea,
    LawFirmMember,
    FirmSetting,
)
from apps.staff.models.staff import Staff
from apps.common.choices import FirmRole
from apps.firm.services.law_firm_service import LawFirmService


# =========================================================
# CONFIGURATION (ONLY PLACE YOU EDIT IN DEPLOYMENT)
# =========================================================

FIRM_DATA = {
    "owner_email": "admin@email.com",

    "firm": {
        "name": "Prime Law Advocates",
        "registration_number": "REG-001",
        "kra_pin": "",
        "email": "info@primelaw.com",
        "phone_number": "+254700000000",
        "website": "",
        "physical_address": "Nairobi, Kenya",
        "postal_address": "",
        "description": "Full-service commercial law firm",
    },

    "branches": [
        {
            "name": "Nairobi Head Office",
            "code": "NBO-001",
            "email": "nairobi@primelaw.com",
            "phone_number": "+254700000000",
            "physical_address": "Nairobi CBD",
            "postal_address": "00100 Nairobi",
            "is_head_office": True,
        }
    ],

    "departments": [
        {"name": "Litigation", "description": ""},
        {"name": "Corporate", "description": ""},
        {"name": "Finance", "description": ""},
    ],

    "practice_areas": [
        {"name": "Criminal Law"},
        {"name": "Commercial Law"},
        {"name": "Employment Law"},
    ],

    "staff": {
        "staff_number": "ADM001",
        "job_title": "Managing Partner",
    }
}


# =========================================================
# BOOTSTRAP LOGIC
# =========================================================

@transaction.atomic
def run():
    owner_email = FIRM_DATA["owner_email"]

    # -----------------------------------------------------
    # 1. Ensure admin exists
    # -----------------------------------------------------
    try:
        owner = User.objects.get(email=owner_email)
    except User.DoesNotExist:
        raise Exception(
            f"Owner user '{owner_email}' does not exist. "
            "Create superuser first before running bootstrap."
        )

    # -----------------------------------------------------
    # 2. Idempotency guard
    # -----------------------------------------------------
    if LawFirm.objects.filter(owner=owner).exists():
        print("⚠️ Firm already exists. Skipping bootstrap.")
        return

    # -----------------------------------------------------
    # 3. Create firm (single source of truth)
    # -----------------------------------------------------
    firm = LawFirmService.create_firm(
        owner=owner,
        validated_data=FIRM_DATA["firm"],
    )

    # -----------------------------------------------------
    # 4. Create or get branches
    # -----------------------------------------------------
    branch_map = {}

    for b in FIRM_DATA["branches"]:
        branch, _ = Branch.objects.get_or_create(
            firm=firm,
            name=b["name"],
            defaults=b,
        )
        branch_map[b["name"]] = branch

    # -----------------------------------------------------
    # 5. Identify head office
    # -----------------------------------------------------
    head_office = next(
        (b for b in branch_map.values() if b.is_head_office),
        None
    )

    if not head_office:
        raise Exception("No head office branch defined. At least one branch must have is_head_office=True.")

    # -----------------------------------------------------
    # 6. Create or get departments
    # -----------------------------------------------------
    for d in FIRM_DATA["departments"]:
        Department.objects.get_or_create(
            firm=firm,
            name=d["name"],
            defaults={
                **d,
                "branch": head_office,
            },
        )

    # -----------------------------------------------------
    # 7. Create or get practice areas
    # -----------------------------------------------------
    for p in FIRM_DATA["practice_areas"]:
        PracticeArea.objects.get_or_create(
            firm=firm,
            name=p["name"],
            defaults=p,
        )

    # -----------------------------------------------------
    # 8. Firm settings (OneToOne safe)
    # -----------------------------------------------------
    FirmSetting.objects.get_or_create(
        firm=firm
    )

    # -----------------------------------------------------
    # 9. Firm membership (idempotent)
    # -----------------------------------------------------
    LawFirmMember.objects.get_or_create(
        firm=firm,
        user=owner,
        defaults={
            "role": FirmRole.LAWYER,
            "created_by": owner,
            "is_active": True,
        },
    )

    # -----------------------------------------------------
    # 10. Staff profile (idempotent)
    # -----------------------------------------------------
    Staff.objects.get_or_create(
        user=owner,
        law_firm=firm,
        defaults={
            "staff_number": FIRM_DATA["staff"]["staff_number"],
            "firm_role": FirmRole.LAWYER,
            "job_title": FIRM_DATA["staff"]["job_title"],
            "date_hired": date.today(),
        },
    )

    # -----------------------------------------------------
    # 11. Output summary
    # -----------------------------------------------------
    print("\n✅ ===== FIRM BOOTSTRAP COMPLETE =====")
    print(f"Firm: {firm.name}")
    print(f"Owner: {owner.email}")
    print(f"Branches: {firm.branches.count()}")
    print(f"Departments: {firm.departments.count()}")
    print(f"Practice Areas: {firm.practice_areas.count()}")
    print("=====================================\n")


# Optional direct execution
if __name__ == "__main__":
    run()
