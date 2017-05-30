from spargo.api.views import SessionAPIView
from spargo.api.auth.utils import success_response

from rest_framework import status
from rest_framework.response import Response


class SyncData(SessionAPIView):
    def get(self, request):
        response = success_response(request.user, request.session.session_key)
        return Response(response, status=status.HTTP_200_OK)
