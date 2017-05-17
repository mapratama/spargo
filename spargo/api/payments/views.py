from rest_framework import status
from rest_framework.response import Response

from spargo.api.response import ErrorResponse
from spargo.core.serializers import serialize_order

from .forms import PaymentSerializer

from rest_framework.views import APIView


class Add(APIView):
    serializer_class = PaymentSerializer

    def post(self, request):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()
            return Response(serialize_order(order), status=status.HTTP_201_CREATED)
        return ErrorResponse(serializer=serializer.errors)
