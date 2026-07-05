from rest_framework import serializers


class ClientProfileSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    full_name = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)
    phone_number = serializers.CharField(read_only=True)
    client_type = serializers.CharField(read_only=True)
    lifecycle_status = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
