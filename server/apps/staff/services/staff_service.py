class StaffService:

    # ==========
    # Retrieval
    # ==========

    @staticmethod
    def list_staff(
        law_firm,
        firm_role=None,
        employment_status=None,
        search=None,
    ):
        """
        Return staff queryset.
        """

    @staticmethod
    def get_staff(
        staff_id,
        law_firm,
    ):
        """
        Return one staff member.
        """

    # ==========
    # Creation
    # ==========

    @staticmethod
    def create_staff(
        *,
        law_firm,
        validated_data,
        created_by,
    ):
        """
        Create User + Staff.
        """

    # ==========
    # Updates
    # ==========

    @staticmethod
    def update_staff(
        *,
        staff,
        validated_data,
        updated_by,
    ):
        """
        Update staff profile.
        """

    # ==========
    # Deletion
    # ==========

    @staticmethod
    def delete_staff(
        *,
        staff,
        deleted_by,
    ):
        """
        Soft delete a staff member.
        """

    # ==========
    # Status
    # ==========

    @staticmethod
    def activate_staff(
        *,
        staff,
        updated_by,
    ):
        """
        Activate employment.
        """

    @staticmethod
    def deactivate_staff(
        *,
        staff,
        updated_by,
    ):
        """
        Deactivate employment.
        """

    @staticmethod
    def change_employment_status(
        *,
        staff,
        status,
        updated_by,
        reason=None,
    ):
        """
        ACTIVE
        ON_LEAVE
        SUSPENDED
        TERMINATED
        RESIGNED
        RETIRED
        """

    # ==========
    # Utility
    # ==========

    @staticmethod
    def generate_staff_number(
        law_firm,
    ):
        """
        Generate unique staff number.
        """

    @staticmethod
    def assign_default_password():
        """
        Generate initial password.
        """

    @staticmethod
    def send_welcome_email(
        user,
        password,
    ):
        """
        Send onboarding email.
        """