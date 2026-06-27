from django.shortcuts import get_object_or_404

from apps.clients.models import Client


class ClientService:

    @staticmethod
    def get_all_clients(user):
        return (
            Client.objects
            .filter(firm=user.firm)
            .order_by("-created_at")
        )

    @staticmethod
    def get_client_by_id(client_id, user):
        return get_object_or_404(
            Client,
            id=client_id,
            firm=user.firm,
        )

    @staticmethod
    def create_client(**validated_data):
        """
        ⚠️ KEEP THIS ONLY FOR SIMPLE CLIENT CREATION (LEGACY SUPPORT)
        Onboarding should NOT use this directly anymore.
        """
        return Client.objects.create(**validated_data)

    @staticmethod
    def update_client(client, **validated_data):
        for field, value in validated_data.items():
            setattr(client, field, value)

        client.save()
        return client

    @staticmethod
    def delete_client(client):
        client.delete()