from django.db import transaction

from apps.users.models import User
from apps.staff.models.staff import Staff
from apps.common.choices import EmploymentStatus, UserRole
from apps.users.services.auth_service import AuthService
from apps.firms.models.firm_member import LawFirmMember


class StaffService:
    """
    Handles:
    - User creation
    - Staff profile creation
    - onboarding (temp password)
    - staff lifecycle management
    """

    # =========================================================
    # RETRIEVAL
    # =========================================================

    @staticmethod
    def list_staff(
        law_firm,
        firm_role=None,
        employment_status=None,
        search=None,
    ):
        qs = Staff.objects.filter(law_firm=law_firm)

        if firm_role:
            qs = qs.filter(firm_role=firm_role)

        if employment_status:
            qs = qs.filter(employment_status=employment_status)

        if search:
            qs = (
                qs.filter(user__first_name__icontains=search)
                | qs.filter(user__last_name__icontains=search)
                | qs.filter(user__email__icontains=search)
            )

        return qs.select_related("user", "law_firm")

    @staticmethod
    def get_staff(staff_id, law_firm):
        return Staff.objects.select_related("user", "law_firm").get(
            id=staff_id,
            law_firm=law_firm,
        )


    # =========================================================
    # CREATION (FINAL)
    # =========================================================
    @staticmethod
    @transaction.atomic
    def create_staff(
        *,
        law_firm,
        validated_data,
        created_by,
    ):
        """
        Creates:
        1. User (with temp password)
        2. Staff profile
        3. LawFirmMember (CRITICAL for login + permissions)
        4. Returns staff + temp password
        """

        # -----------------------------------------------------
        # 1. Create User (centralized auth service)
        # -----------------------------------------------------
        user, temp_password = AuthService.create_user_with_temp_password(
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            phone_number=validated_data["phone_number"],
            national_id_number=validated_data["national_id_number"],
            role=UserRole.STAFF,
        )

        # -----------------------------------------------------
        # 2. Create Staff profile
        # -----------------------------------------------------
        staff = Staff.objects.create(
            user=user,
            law_firm=law_firm,
            staff_number=StaffService.generate_staff_number(law_firm),
            firm_role=validated_data["firm_role"],
            department=validated_data.get("department"),
            job_title=validated_data["job_title"],
            work_email=validated_data.get("work_email"),
            work_phone=validated_data.get("work_phone"),
            office_location=validated_data.get("office_location"),
            reports_to=validated_data.get("reports_to"),
            employment_type=validated_data.get("employment_type"),
            date_hired=validated_data["date_hired"],
            employment_status=EmploymentStatus.ACTIVE,
            is_active=True,
        )

        # -----------------------------------------------------
        # 3. Create Law Firm Membership (IMPORTANT FIX)
        # -----------------------------------------------------
        LawFirmMember.objects.create(
            firm=law_firm,
            user=user,
            role=validated_data["firm_role"],
            created_by=created_by,
            is_active=True,
        )

        # -----------------------------------------------------
        # 4. Send onboarding email (optional)
        # -----------------------------------------------------
        StaffService.send_welcome_email(user, temp_password)

        return staff, temp_password

    # =========================================================
    # UTILITY
    # =========================================================
    @staticmethod
    def generate_staff_number(law_firm):
        count = Staff.objects.filter(law_firm=law_firm).count() + 1
        return f"STF-{count:04d}"

    @staticmethod
    def send_welcome_email(user, password):
        print(f"[WELCOME EMAIL] {user.email} | temp password: {password}")

    # =========================================================
    # UPDATE
    # =========================================================

    @staticmethod
    def update_staff(*, staff, validated_data, updated_by):
        for attr, value in validated_data.items():
            setattr(staff, attr, value)

        staff.save()
        return staff

    # =========================================================
    # DELETE (soft)
    # =========================================================

    @staticmethod
    def delete_staff(*, staff, deleted_by):
        staff.is_active = False
        staff.employment_status = EmploymentStatus.RESIGNED
        staff.save()
        return staff

    # =========================================================
    # STATUS MANAGEMENT
    # =========================================================

    @staticmethod
    def activate_staff(*, staff, updated_by):
        staff.is_active = True
        staff.employment_status = EmploymentStatus.ACTIVE
        staff.save()
        return staff

    @staticmethod
    def deactivate_staff(*, staff, updated_by):
        staff.is_active = False
        staff.employment_status = EmploymentStatus.SUSPENDED
        staff.save()
        return staff

    @staticmethod
    def change_employment_status(
        *,
        staff,
        status,
        updated_by,
        reason=None,
    ):
        staff.employment_status = status
        staff.save()
        return staff

    # =========================================================
    # UTILITIES
    # =========================================================

    @staticmethod
    def generate_staff_number(law_firm):
        count = Staff.objects.filter(law_firm=law_firm).count() + 1
        return f"STF-{count:04d}"

    @staticmethod
    def send_welcome_email(user, password):
        """
        Replace with real email backend later.
        """
        print(f"[WELCOME EMAIL] {user.email} | temp password: {password}")