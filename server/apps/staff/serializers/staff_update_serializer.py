from rest_framework import serializers

from apps.staff.models.staff import Staff
from apps.common.choices import (
    EmploymentStatus,
    EmploymentType,
    FirmRole,
)


class StaffUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = [
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
        ]

    def validate_firm_role(self, value):
        if value not in FirmRole.values:
            raise serializers.ValidationError(
                "Invalid firm role."
            )
        return value

    def validate_employment_type(self, value):
        if value not in EmploymentType.values:
            raise serializers.ValidationError(
                "Invalid employment type."
            )
        return value

    def validate_employment_status(self, value):
        if value not in EmploymentStatus.values:
            raise serializers.ValidationError(
                "Invalid employment status."
            )
        return value