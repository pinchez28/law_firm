from rest_framework import serializers

from apps.common.choices import EmploymentType, FirmRole
from apps.staff.models.staff import Staff
from apps.users.models import User


class StaffCreateSerializer(serializers.ModelSerializer):
    # User fields
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    phone_number = serializers.CharField(max_length=20)
    national_id_number = serializers.CharField(max_length=20)

    class Meta:
        model = Staff
        fields = [
            # User
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "national_id_number",

            # Staff
            "firm_role",
            "department",
            "job_title",
            "work_email",
            "work_phone",
            "office_location",
            "reports_to",
            "employment_type",
            "date_hired",
        ]

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(
                "A user with this email already exists."
            )
        return value

    def validate_phone_number(self, value):
        if User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError(
                "A user with this phone number already exists."
            )
        return value

    def validate_national_id_number(self, value):
        if User.objects.filter(
            national_id_number=value
        ).exists():
            raise serializers.ValidationError(
                "A user with this national ID number already exists."
            )
        return value

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