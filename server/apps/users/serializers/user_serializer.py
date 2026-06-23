from rest_framework import serializers
from apps.users.models.user import User


class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "email", "role", "full_name"]

    def get_role(self, obj):
        return obj.role.upper() if obj.role else None