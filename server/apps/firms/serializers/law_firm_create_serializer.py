from rest_framework import serializers


class LawFirmCreateSerializer(serializers.Serializer):

    name = serializers.CharField(
        max_length=255,
    )

    registration_number = serializers.CharField(
        required=False,
        allow_blank=True,
    )

    email = serializers.EmailField(
        required=False,
        allow_blank=True,
    )

    phone_number = serializers.CharField(
        required=False,
        allow_blank=True,
    )

    address = serializers.CharField(
        required=False,
        allow_blank=True,
    )