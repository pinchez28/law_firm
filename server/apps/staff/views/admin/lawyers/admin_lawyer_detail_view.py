from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.staff.serializers.staff_detail_serializer import StaffDetailSerializer
from apps.staff.services.staff_service import StaffService
from apps.staff.models.staff import Staff


class AdminLawyerDetailView(APIView):

    def get(self, request, lawyer_id):
        law_firm = request.user.staff_profile.law_firm

        lawyer = StaffService.get_staff(
            staff_id=lawyer_id,
            law_firm=law_firm,
        )

        # -----------------------------
        # Direct reports (this lawyer only)
        # -----------------------------
        direct_reports_qs = Staff.objects.filter(
            reports_to=lawyer
        ).select_related("user")

        # -----------------------------
        # PERSONAL analytics ONLY
        # -----------------------------
        today = timezone.now().date()

        tenure_days = None
        if lawyer.date_hired:
            tenure_days = (
                (lawyer.date_terminated or today) - lawyer.date_hired
            ).days

        # optional personal stats
        is_new_hire = tenure_days is not None and tenure_days <= 30

        serializer = StaffDetailSerializer(lawyer)

        return Response(
            {
                "lawyer": serializer.data,

                # 👇 STRUCTURE (PERSONAL)
                "manager": (
                    lawyer.reports_to.user.full_name
                    if lawyer.reports_to else None
                ),
                "direct_reports_count": direct_reports_qs.count(),
                "direct_reports": StaffDetailSerializer(
                    direct_reports_qs,
                    many=True
                ).data,

                # 👇 PERSONAL METRICS ONLY
                "analytics": {
                # -----------------------------
                # TENURE INTELLIGENCE
                # -----------------------------
                "tenure_days": tenure_days,
                "tenure_category": (
                    "new_joiner" if tenure_days and tenure_days <= 30 else
                    "rising_lawyer" if tenure_days and tenure_days <= 180 else
                    "established" if tenure_days and tenure_days <= 730 else
                    "veteran"
                ),

                # -----------------------------
                # LEADERSHIP SIGNAL
                # -----------------------------
                "is_team_lead": direct_reports_qs.exists(),
                "team_size": direct_reports_qs.count(),
                "leadership_level": (
                    "none" if not direct_reports_qs.exists()
                    else "small_team" if direct_reports_qs.count() <= 3
                    else "senior_lead"
                ),

                # -----------------------------
                # OPERATIONAL READINESS SCORE
                # -----------------------------
                "operational_readiness_score": round(
                    (
                        sum([
                            bool(lawyer.employee_number),
                            bool(lawyer.work_email),
                            bool(lawyer.work_phone),
                            bool(lawyer.department),
                            bool(lawyer.office_location),
                            lawyer.is_active,
                        ]) / 6
                    ) * 100,
                    2
                ),

                # -----------------------------
                # ONBOARDING QUALITY FLAG
                # -----------------------------
                "onboarding_status": (
                    "complete" if lawyer.work_email and lawyer.work_phone and lawyer.employee_number
                    else "partial"
                ),

                # -----------------------------
                # ENGAGEMENT SIGNAL (proxy)
                # -----------------------------
                "engagement_risk": (
                    "low_risk" if lawyer.is_active and lawyer.work_email
                    else "needs_attention"
                ),

                # -----------------------------
                # ROLE CONTEXT
                # -----------------------------
                "role": lawyer.firm_role,
                "is_senior_role": lawyer.firm_role in [
                    "MANAGING_PARTNER",
                    "PARTNER"
                ],
            }
            },
            status=status.HTTP_200_OK,
        )