from django.shortcuts import get_object_or_404

from apps.clients.models import Client


class ClientService:

    @staticmethod
    def get_all_clients():
        return Client.objects.all()

    @staticmethod
    def get_client_by_id(client_id):
        return get_object_or_404(
            Client,
            id=client_id,
        )

    @staticmethod
    def create_client(**validated_data):
        return Client.objects.create(
            **validated_data
        )

    @staticmethod
    def update_client(
        client,
        **validated_data,
    ):
        for field, value in validated_data.items():
            setattr(
                client,
                field,
                value,
            )

        client.save()

        return client

    @staticmethod
    def delete_client(client):
        client.delete()