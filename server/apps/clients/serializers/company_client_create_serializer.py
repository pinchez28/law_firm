from rest_framework import serializers

from apps.clients.models import Client, CompanyClient


class CompanyClientCreateSerializer(serializers.Serializer):

    # ----------------------------
    # Core Company Info
    # ----------------------------
    company_name = serializers.CharField(max_length=255)
    registration_number = serializers.CharField(max_length=100)

    tax_pin = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    incorporation_date = serializers.DateField(required=False, allow_null=True)
    country_of_incorporation = serializers.CharField(required=False, allow_blank=True)

    industry = serializers.CharField(required=False, allow_blank=True)

    director_count = serializers.IntegerField(required=False, default=0)

    company_status = serializers.CharField(required=False, allow_blank=True)

    # ----------------------------
    # Client Base Fields
    # ----------------------------
    onboarding_type = serializers.ChoiceField(
        choices=Client.OnboardingType.choices
    )

    portal_enabled = serializers.BooleanField(default=False)

    full_name = serializers.CharField(required=False, allow_blank=True)

    email = serializers.EmailField(required=False, allow_null=True)
    phone_number = serializers.CharField(required=False, allow_blank=True)

    # ----------------------------
    # Address (for ClientAddress model)
    # ----------------------------
    country = serializers.CharField()
    county = serializers.CharField(required=False, allow_blank=True)
    city = serializers.CharField(required=False, allow_blank=True)
    street = serializers.CharField(required=False, allow_blank=True)
    postal_code = serializers.CharField(required=False, allow_blank=True)
    full_address = serializers.CharField()