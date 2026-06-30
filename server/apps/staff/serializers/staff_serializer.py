from rest_framework import serializers

from apps.staff.models.staff import Staff


class StaffSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(
        source="user.full_name",
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
    first_name = serializers.CharField(
        source="user.first_name",
        read_only=True,
    )
    last_name = serializers.CharField(
        source="user.last_name",
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
            "firm_role",
            "department",
            "job_title",
            "work_email",
            "work_phone",
            "employment_type",
            "employment_status",
            "date_hired",
            "is_active",
        ]
        read_only_fields = fields