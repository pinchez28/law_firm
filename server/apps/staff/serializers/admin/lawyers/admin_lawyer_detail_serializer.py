from rest_framework import serializers

from apps.staff.models.lawyer import Lawyer


class AdminLawyerDetailSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source="user.full_name", read_only=True)
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)
    phone_number = serializers.CharField(source="user.phone_number", read_only=True)
    national_id_number = serializers.CharField(
        source="user.national_id_number",
        read_only=True,
    )

    law_firm_name = serializers.CharField(source="law_firm.name", read_only=True)
    reports_to_name = serializers.CharField(
        source="reports_to.user.full_name",
        read_only=True,
    )
    practice_areas = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Lawyer
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
            "law_firm_name",
            "firm_role",
            "department",
            "job_title",
            "work_email",
            "work_phone",
            "office_location",
            "reports_to",
            "reports_to_name",
            "admission_number",
            "practicing_certificate_number",
            "bar_admission_date",
            "practice_areas",
            "is_notary",
            "can_commission_oaths",
            "is_court_approved",
            "employment_type",
            "employment_status",
            "date_hired",
            "probation_end_date",
            "date_terminated",
            "termination_reason",
            "professional_summary",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields