from dataclasses import dataclass
from datetime import date
from collections import defaultdict, Counter
from typing import Dict, List, Optional, Any, Tuple

from django.db.models import QuerySet

from apps.staff.models.staff import Staff
from apps.common.choices import EmploymentStatus, EmploymentType, FirmRole


@dataclass
class StaffAnalyticsSummary:
    total_staff: int
    active_staff: int
    inactive_staff: int
    terminated_staff: int
    on_probation: int


class StaffAnalyticsService:
    """
    Centralized analytics engine for Staff data.

    Used for:
    - Admin dashboards
    - HR reporting
    - Organizational insights
    """

    def __init__(self, queryset: Optional[QuerySet] = None):
        self.queryset = queryset or Staff.objects.select_related("user", "reports_to")

    # -----------------------------
    # CORE FILTERS
    # -----------------------------

    def base_queryset(self, law_firm_id: Optional[str] = None) -> QuerySet:
        qs = self.queryset
        if law_firm_id:
            qs = qs.filter(law_firm_id=law_firm_id)
        return qs

    # -----------------------------
    # SUMMARY METRICS
    # -----------------------------

    def get_summary(self, law_firm_id: Optional[str] = None) -> StaffAnalyticsSummary:
        qs = self.base_queryset(law_firm_id)

        total = qs.count()
        active = qs.filter(employment_status=EmploymentStatus.ACTIVE).count()
        inactive = qs.filter(is_active=False).count()
        terminated = qs.filter(employment_status=EmploymentStatus.TERMINATED).count()

        today = date.today()
        on_probation = qs.filter(
            probation_end_date__isnull=False,
            probation_end_date__gte=today
        ).count()

        return StaffAnalyticsSummary(
            total_staff=total,
            active_staff=active,
            inactive_staff=inactive,
            terminated_staff=terminated,
            on_probation=on_probation,
        )

    # -----------------------------
    # DISTRIBUTIONS
    # -----------------------------

    def get_department_distribution(self, law_firm_id: Optional[str] = None) -> Dict[str, int]:
        qs = self.base_queryset(law_firm_id)

        distribution = defaultdict(int)
        for staff in qs:
            key = staff.department or "Unassigned"
            distribution[key] += 1

        return dict(distribution)

    def get_role_distribution(self, law_firm_id: Optional[str] = None) -> Dict[str, int]:
        qs = self.base_queryset(law_firm_id)

        counter = Counter()
        for staff in qs:
            counter[staff.firm_role] += 1

        return dict(counter)

    def get_employment_type_distribution(self, law_firm_id: Optional[str] = None) -> Dict[str, int]:
        qs = self.base_queryset(law_firm_id)

        counter = Counter()
        for staff in qs:
            counter[staff.employment_type] += 1

        return dict(counter)

    def get_employment_status_distribution(self, law_firm_id: Optional[str] = None) -> Dict[str, int]:
        qs = self.base_queryset(law_firm_id)

        counter = Counter()
        for staff in qs:
            counter[staff.employment_status] += 1

        return dict(counter)

    # -----------------------------
    # TENURE ANALYTICS
    # -----------------------------

    def get_tenure_analysis(self, law_firm_id: Optional[str] = None) -> Dict[str, Any]:
        qs = self.base_queryset(law_firm_id)

        today = date.today()

        tenures = []
        for staff in qs:
            if not staff.date_hired:
                continue

            end_date = staff.date_terminated or today
            tenure_days = (end_date - staff.date_hired).days
            tenures.append(tenure_days)

        if not tenures:
            return {
                "average_tenure_days": 0,
                "min_tenure_days": 0,
                "max_tenure_days": 0,
                "total_analyzed": 0,
            }

        return {
            "average_tenure_days": sum(tenures) / len(tenures),
            "min_tenure_days": min(tenures),
            "max_tenure_days": max(tenures),
            "total_analyzed": len(tenures),
        }

    # -----------------------------
    # HIRING TRENDS
    # -----------------------------

    def get_hiring_trends(self, law_firm_id: Optional[str] = None) -> Dict[str, int]:
        qs = self.base_queryset(law_firm_id)

        trends = defaultdict(int)

        for staff in qs:
            if not staff.date_hired:
                continue
            key = staff.date_hired.strftime("%Y-%m")
            trends[key] += 1

        return dict(sorted(trends.items()))

    # -----------------------------
    # OFFICE DISTRIBUTION
    # -----------------------------

    def get_office_location_distribution(self, law_firm_id: Optional[str] = None) -> Dict[str, int]:
        qs = self.base_queryset(law_firm_id)

        counter = Counter()
        for staff in qs:
            location = staff.office_location or "Unassigned"
            counter[location] += 1

        return dict(counter)

    # -----------------------------
    # REPORTING STRUCTURE
    # -----------------------------

    def get_reporting_structure(self, law_firm_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Builds a lightweight org structure map:
        - managers -> direct reports count
        """

        qs = self.base_queryset(law_firm_id)

        structure = defaultdict(list)

        for staff in qs:
            manager = staff.reports_to.user.full_name if staff.reports_to else "No Manager"
            structure[manager].append(staff.user.full_name)

        return {
            manager: {
                "team_size": len(reports),
                "team_members": reports
            }
            for manager, reports in structure.items()
        }

    # -----------------------------
    # PERFORMANCE METRICS HELPERS
    # -----------------------------

    def get_active_ratio(self, law_firm_id: Optional[str] = None) -> float:
        qs = self.base_queryset(law_firm_id)

        total = qs.count()
        if total == 0:
            return 0.0

        active = qs.filter(employment_status=EmploymentStatus.ACTIVE).count()
        return active / total

    def get_termination_rate(self, law_firm_id: Optional[str] = None) -> float:
        qs = self.base_queryset(law_firm_id)

        total = qs.count()
        if total == 0:
            return 0.0

        terminated = qs.filter(employment_status=EmploymentStatus.TERMINATED).count()
        return terminated / total

    # -----------------------------
    # COMBINED DASHBOARD PAYLOAD
    # -----------------------------

    def get_dashboard(self, law_firm_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Single-call payload for admin dashboards.
        """

        return {
            "summary": self.get_summary(law_firm_id).__dict__,
            "department_distribution": self.get_department_distribution(law_firm_id),
            "role_distribution": self.get_role_distribution(law_firm_id),
            "employment_type_distribution": self.get_employment_type_distribution(law_firm_id),
            "status_distribution": self.get_employment_status_distribution(law_firm_id),
            "tenure": self.get_tenure_analysis(law_firm_id),
            "hiring_trends": self.get_hiring_trends(law_firm_id),
            "office_distribution": self.get_office_location_distribution(law_firm_id),
            "reporting_structure": self.get_reporting_structure(law_firm_id),
            "ratios": {
                "active_ratio": self.get_active_ratio(law_firm_id),
                "termination_rate": self.get_termination_rate(law_firm_id),
            }
        }