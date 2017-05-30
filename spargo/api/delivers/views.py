from spargo.api.views import SessionAPIView
from spargo.apps.jne.models import JNE
from spargo.apps.j_and_t.models import JAndT
from spargo.core.serializers import serialize_jne, serialize_j_and_t

from rest_framework import status
from rest_framework.response import Response


class ListJNE(SessionAPIView):
    def get(self, request):
        response = [serialize_jne(jne) for jne in JNE.objects.all()]
        return Response(response, status=status.HTTP_200_OK)


class ListJNT(SessionAPIView):
    def get(self, request):
        response = [serialize_j_and_t(j_and_t) for j_and_t in JAndT.objects.all()]
        return Response(response, status=status.HTTP_200_OK)
