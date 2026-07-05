from django.contrib.auth import authenticate

from apps.users.models import User


class LawyerPasswordService:
    @staticmethod
    def change_password(user, current_password, new_password):
        if not authenticate(email=user.email, password=current_password):
            raise ValueError("Current password is incorrect.")

        user.set_password(new_password)
        user.save(update_fields=["password"])
        return user
