from rest_framework import serializers

from apps.common.choices import EmploymentType
from apps.staff.models import Lawyer, Secretary, SecretaryPermission
from apps.users.models import User


class AdminSecretaryCreateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    phone_number = serializers.CharField(max_length=20)
    national_id_number = serializers.CharField(max_length=20)
    staff_number = serializers.CharField(
        max_length=30,
        required=False,
        allow_blank=True,
    )
    assigned_lawyer_ids = serializers.PrimaryKeyRelatedField(
        queryset=Lawyer.objects.all(),
        many=True,
        required=False,
        write_only=True,
    )
    permission_codes = serializers.MultipleChoiceField(
        choices=SecretaryPermission.choices,
        required=False,
        write_only=True,
    )

    class Meta:
        model = Secretary
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "national_id_number",
            "staff_number",
            "employee_number",
            "department",
            "job_title",
            "work_email",
            "work_phone",
            "office_location",
            "reports_to",
            "assigned_lawyer_ids",
            "can_prepare_documents",
            "can_schedule_appointments",
            "can_manage_client_intake",
            "can_receive_documents",
            "permission_codes",
            "employment_type",
            "date_hired",
            "probation_end_date",
            "notes",
        ]

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate_phone_number(self, value):
        if User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError(
                "A user with this phone number already exists."
            )
        return value

    def validate_national_id_number(self, value):
        if User.objects.filter(national_id_number=value).exists():
            raise serializers.ValidationError(
                "A user with this national ID number already exists."
            )
        return value

    def validate_employment_type(self, value):
        if value not in EmploymentType.values:
            raise serializers.ValidationError("Invalid employment type.")
        return value

    def validate(self, attrs):
        law_firm = self.context.get("law_firm")
        reports_to = attrs.get("reports_to")
        assigned_lawyers = attrs.get("assigned_lawyer_ids", [])

        if reports_to and law_firm and reports_to.law_firm_id != law_firm.id:
            raise serializers.ValidationError(
                {"reports_to": "Reporting lawyer must belong to the same law firm."}
            )

        for lawyer in assigned_lawyers:
            if law_firm and lawyer.law_firm_id != law_firm.id:
                raise serializers.ValidationError(
                    {
                        "assigned_lawyer_ids": (
                            "Assigned lawyers must belong to the same law firm."
                        )
                    }
                )

        return attrs
