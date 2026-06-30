from rest_framework import serializers

from apps.staff.models.staff import Staff


class StaffDetailSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(
        source="user.full_name",
        read_only=True,
    )

    first_name = serializers.CharField(
        source="user.first_name",
        read_only=True,
    )

    last_name = serializers.CharField(
        source="user.last_name",
        read_only=True,
    )

    email = serializers.EmailField(
        source="user.email",
        read_only=True,
    )

    phone_number = serializers.CharField(
        source="user.phone_number",
        read_only=True,
    )

    national_id_number = serializers.CharField(
        source="user.national_id_number",
        read_only=True,
    )

    class Meta:
        model = Staff
        fields = [
            "id",
            "staff_number",
            "employee_number",

            "full_name",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "national_id_number",

            "law_firm",
            "firm_role",
            "department",
            "job_title",

            "work_email",
            "work_phone",
            "office_location",

            "reports_to",

            "employment_type",
            "employment_status",

            "date_hired",
            "probation_end_date",
            "date_terminated",
            "termination_reason",

            "is_active",

            "created_at",
            "updated_at",
        ]

        read_only_fields = fields