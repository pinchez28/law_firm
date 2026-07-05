from rest_framework import serializers


class LawyerCaseSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    title = serializers.CharField(read_only=True)
    case_number = serializers.CharField(read_only=True)
    status = serializers.CharField(read_only=True)
    client_name = serializers.CharField(read_only=True)
    practice_area = serializers.CharField(read_only=True)
    assigned_lawyer = serializers.CharField(read_only=True)
    last_updated = serializers.CharField(read_only=True)
