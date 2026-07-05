from rest_framework import serializers


class ClientCaseSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    title = serializers.CharField(read_only=True)
    status = serializers.CharField(read_only=True)
    last_updated = serializers.CharField(read_only=True)
