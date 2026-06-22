from django.contrib.auth import get_user_model

User = get_user_model()


class UserService:

    @staticmethod
    def get_user_profile(user_id):
        return User.objects.select_related().get(id=user_id)

    @staticmethod
    def create_user(data):
        return User.objects.create_user(**data)

    @staticmethod
    def update_user(user, data):
        for key, value in data.items():
            setattr(user, key, value)
        user.save()
        return user