from django.db.models import Count
from django.utils import timezone
from datetime import timedelta

from apps.clients.models import Client



class ClientAnalyticsService:

    @staticmethod
    def get_client_summary():
        total_clients = Client.objects.count()

        active_clients = Client.objects.filter(
            is_active=True
        ).count()

        inactive_clients = Client.objects.filter(
            is_active=False
        ).count()

        portal_enabled_clients = Client.objects.filter(
            portal_enabled=True
        ).count()

        assisted_clients = Client.objects.filter(
            onboarding_type="ASSISTED"
        ).count()

        public_registration_clients = Client.objects.filter(
            onboarding_type="PUBLIC_REGISTRATION"
        ).count()

        firm_created_clients = Client.objects.filter(
            onboarding_type="FIRM_CREATED"
        ).count()

        clients_by_type = (
            Client.objects
            .values("client_type")
            .annotate(total=Count("id"))
        )

        recent_clients = Client.objects.filter(
            created_at__gte=timezone.now() - timedelta(days=30)
        ).count()


        recent_clients = Client.objects.filter(
            created_at__gte=timezone.now() - timedelta(days=30)
        ).count()

        current_month = timezone.now().month
        current_year = timezone.now().year

        new_clients_this_month = Client.objects.filter(
            created_at__month=current_month,
            created_at__year=current_year
        ).count()

        return {
            "total_clients": total_clients,
            "active_clients": active_clients,
            "inactive_clients": inactive_clients,
            "portal_enabled_clients": portal_enabled_clients,
            "assisted_clients": assisted_clients,
            "public_registration_clients": public_registration_clients,
            "firm_created_clients": firm_created_clients,
            "clients_by_type": {
                item["client_type"]: item["total"]
                for item in clients_by_type
            },
            "recent_clients": recent_clients,
            "growth_metrics": {
                "new_clients_this_month": new_clients_this_month,
            }
        }