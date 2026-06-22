from rest_framework.views import APIView
from rest_framework.response import Response

from ..services.user_service import UserService


class UserDetailView(APIView):

    def get(self, request, user_id):
        user = UserService.get_user_profile(user_id)
        return Response({
            "id": user.id,
            "email": user.email,
            "role": user.role
        })