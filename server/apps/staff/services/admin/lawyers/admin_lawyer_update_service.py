from django.db import transaction


class AdminLawyerUpdateService:
    """
    Updates lawyer profile, user identity, and professional details.
    """

    @staticmethod
    @transaction.atomic
    def update_lawyer(*, lawyer, validated_data, updated_by):
        user = lawyer.user

        # User fields
        email = validated_data.pop("email", None)
        phone_number = validated_data.pop("phone_number", None)

        if email is not None:
            user.email = email

        if phone_number is not None:
            user.phone_number = phone_number

        user.save()

        # Lawyer fields
        practice_areas = validated_data.pop("practice_area_ids", None)

        for field, value in validated_data.items():
            setattr(lawyer, field, value)

        lawyer.save()

        if practice_areas is not None:
            lawyer.practice_areas.set(practice_areas)

        return lawyer