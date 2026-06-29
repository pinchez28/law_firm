from apps.users.models import User
from apps.firms.models import LawFirm, LawFirmMember
from apps.common.choices import FirmRole

# -------------------------------------------------
# 1. Get Admin User
# -------------------------------------------------
admin = User.objects.get(email="admin@email.com")

# -------------------------------------------------
# 2. Create Firm
# -------------------------------------------------
firm = LawFirm.objects.create(
    name="Prime Law Advocates",
    registration_number="REG-001",
    email="info@primelaw.com",
    phone_number="+254700000000",
    address="Nairobi, Kenya",
    owner=admin
)

# -------------------------------------------------
# 3. Create Membership (link admin to firm)
# -------------------------------------------------
LawFirmMember.objects.create(
    firm=firm,
    user=admin,
    role=FirmRole.LAWYER,
    created_by=admin,
    is_active=True
)

# -------------------------------------------------
# 4. Verify
# -------------------------------------------------
print("Firm created:", firm)
print("Owner firm:", admin.owned_firm)
print("Members:", firm.members.all())