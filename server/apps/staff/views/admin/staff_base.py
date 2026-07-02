from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.choices import FirmRole
from apps.staff.serializers.staff_change_status_serializer import (
    StaffChangeStatusSerializer,
)
from apps.staff.serializers.staff_create_serializer import (
    StaffCreateSerializer,
)
from apps.staff.serializers.staff_detail_serializer import (
    StaffDetailSerializer,
)
from apps.staff.serializers.staff_update_serializer import (
    StaffUpdateSerializer,
)
from apps.staff.services.staff_service import StaffService
from apps.staff.serializers.staff_serializer import StaffSerializer
from apps.staff.models.staff import Staff


class AdminStaffListView(APIView):
    firm_role = None

    def get(self, request):
        result = StaffService.list_staff(
            law_firm=request.user.staff_profile.law_firm,
            firm_role=self.firm_role,
        )

        staff_qs = result["queryset"]
        analytics = result["analytics"]

        serializer = StaffSerializer(staff_qs, many=True)

        return Response(
            {
                "summary": analytics.get_dashboard(),
                "staff": serializer.data,
                "metadata": {"total_records": staff_qs.count()},
            },
            status=status.HTTP_200_OK,
        )


class AdminStaffCreateView(APIView):
    firm_role = None

    def post(self, request):
        data = request.data.copy()

        if self.firm_role and not isinstance(self.firm_role, (list, tuple)):
            data["firm_role"] = self.firm_role

        serializer = StaffCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        staff, temp_password = StaffService.create_staff(
            law_firm=request.user.staff_profile.law_firm,
            validated_data=serializer.validated_data,
            created_by=request.user,
        )

        return Response(
            {
                "staff": StaffDetailSerializer(staff).data,
                "temp_password": temp_password,
            },
            status=status.HTTP_201_CREATED,
        )


class AdminStaffDetailView(APIView):
    firm_role = None

    def get(self, request, staff_id):
        staff_member = StaffService.get_staff(
            staff_id=staff_id,
            law_firm=request.user.staff_profile.law_firm,
            firm_role=self.firm_role,
        )

        direct_reports_qs = Staff.objects.filter(
            reports_to=staff_member
        ).select_related("user")

        today = timezone.now().date()
        tenure_days = None
        if staff_member.date_hired:
            tenure_days = (
                (staff_member.date_terminated or today) -
                staff_member.date_hired
            ).days

        serializer = StaffDetailSerializer(staff_member)

        return Response(
            {
                "staff": serializer.data,
                "manager": (
                    staff_member.reports_to.user.full_name
                    if staff_member.reports_to else None
                ),
                "direct_reports_count": direct_reports_qs.count(),
                "direct_reports": StaffDetailSerializer(
                    direct_reports_qs,
                    many=True,
                ).data,
                "analytics": {
                    "tenure_days": tenure_days,
                    "tenure_category": (
                        "new_joiner" if tenure_days and tenure_days <= 30 else
                        "rising_staff" if tenure_days and tenure_days <= 180 else
                        "established" if tenure_days and tenure_days <= 730 else
                        "veteran"
                    ),
                    "is_team_lead": direct_reports_qs.exists(),
                    "team_size": direct_reports_qs.count(),
                    "leadership_level": (
                        "none" if not direct_reports_qs.exists()
                        else "small_team" if direct_reports_qs.count() <= 3
                        else "senior_lead"
                    ),
                    "operational_readiness_score": round(
                        (
                            sum([
                                bool(staff_member.employee_number),
                                bool(staff_member.work_email),
                                bool(staff_member.work_phone),
                                bool(staff_member.department),
                                bool(staff_member.office_location),
                                staff_member.is_active,
                            ]) / 6
                        ) * 100,
                        2,
                    ),
                    "onboarding_status": (
                        "complete" if staff_member.work_email and staff_member.work_phone and staff_member.employee_number
                        else "partial"
                    ),
                    "engagement_risk": (
                        "low_risk" if staff_member.is_active and staff_member.work_email
                        else "needs_attention"
                    ),
                    "role": staff_member.firm_role,
                },
            },
            status=status.HTTP_200_OK,
        )


class AdminStaffUpdateView(APIView):
    firm_role = None

    def patch(self, request, staff_id):
        staff_member = StaffService.get_staff(
            staff_id=staff_id,
            law_firm=request.user.staff_profile.law_firm,
            firm_role=self.firm_role,
        )

        serializer = StaffUpdateSerializer(
            staff_member,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        staff_member = StaffService.update_staff(
            staff=staff_member,
            validated_data=serializer.validated_data,
            updated_by=request.user,
        )

        return Response(
            StaffDetailSerializer(staff_member).data,
            status=status.HTTP_200_OK,
        )


class AdminStaffDeleteView(APIView):
    firm_role = None

    def delete(self, request, staff_id):
        staff_member = StaffService.get_staff(
            staff_id=staff_id,
            law_firm=request.user.staff_profile.law_firm,
            firm_role=self.firm_role,
        )

        StaffService.delete_staff(
            staff=staff_member,
            deleted_by=request.user,
        )

        return Response({"detail": "Staff member deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


class AdminStaffActivateView(APIView):
    firm_role = None

    def post(self, request, staff_id):
        staff_member = StaffService.get_staff(
            staff_id=staff_id,
            law_firm=request.user.staff_profile.law_firm,
            firm_role=self.firm_role,
        )

        staff_member = StaffService.activate_staff(
            staff=staff_member,
            updated_by=request.user,
        )

        return Response(
            StaffDetailSerializer(staff_member).data,
            status=status.HTTP_200_OK,
        )


class AdminStaffDeactivateView(APIView):
    firm_role = None

    def post(self, request, staff_id):
        staff_member = StaffService.get_staff(
            staff_id=staff_id,
            law_firm=request.user.staff_profile.law_firm,
            firm_role=self.firm_role,
        )

        staff_member = StaffService.deactivate_staff(
            staff=staff_member,
            updated_by=request.user,
        )

        return Response(
            StaffDetailSerializer(staff_member).data,
            status=status.HTTP_200_OK,
        )


class AdminStaffChangeStatusView(APIView):
    firm_role = None

    def post(self, request, staff_id):
        staff_member = StaffService.get_staff(
            staff_id=staff_id,
            law_firm=request.user.staff_profile.law_firm,
            firm_role=self.firm_role,
        )

        serializer = StaffChangeStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        staff_member = StaffService.change_employment_status(
            staff=staff_member,
            status=serializer.validated_data["employment_status"],
            reason=serializer.validated_data.get("termination_reason"),
            updated_by=request.user,
        )

        return Response(
            StaffDetailSerializer(staff_member).data,
            status=status.HTTP_200_OK,
        )
