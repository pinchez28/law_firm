from django.db import transaction

from apps.common.choices import EmploymentStatus, FirmRole, UserRole
from apps.firm.models.firm_member import LawFirmMember
from apps.staff.models.lawyer import Lawyer
from apps.staff.services.admin.lawyers.admin_lawyer_number_service import (
    AdminLawyerNumberService,
)
from apps.users.services.auth_service import AuthService


class AdminLawyerCreateService:
    """
    Creates a lawyer from the admin side.

    This creates:
    - User
    - Lawyer profile
    - Law firm membership
    """

    @staticmethod
    @transaction.atomic
    def create_lawyer(*, law_firm, validated_data, created_by):
        practice_areas = validated_data.pop("practice_area_ids", [])

        user, temp_password = AuthService.create_user_with_temp_password(
            email=validated_data.pop("email"),
            first_name=validated_data.pop("first_name"),
            last_name=validated_data.pop("last_name"),
            phone_number=validated_data.pop("phone_number"),
            national_id_number=validated_data.pop("national_id_number"),
            role=UserRole.STAFF,
        )

        staff_number = validated_data.get("staff_number")
        if not staff_number:
            staff_number = AdminLawyerNumberService.generate_staff_number(law_firm)

            print(validated_data)

        lawyer = Lawyer.objects.create(
            user=user,
            law_firm=law_firm,
            firm_role=FirmRole.LAWYER,
            employment_status=EmploymentStatus.ACTIVE,
            is_active=True,
            **validated_data,
        )

        if practice_areas:
            lawyer.practice_areas.set(practice_areas)

        LawFirmMember.objects.create(
            firm=law_firm,
            user=user,
            role=FirmRole.LAWYER,
            created_by=created_by,
            is_active=True,
        )

        return lawyer, temp_password