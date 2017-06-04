from spargo.api.response import ErrorResponse
from spargo.api.views import SessionAPIView
from spargo.apps.products.models import Product
from spargo.core.serializers import serialize_product

from rest_framework import status
from rest_framework.response import Response


class Details(SessionAPIView):
    def get(self, request, id):
        from time import sleep

        sleep(5)

        try:
            product = Product.objects.get(id=id)
        except Product.DoesNotExist:
            return ErrorResponse(error_description='Product Not Found')

        return Response(serialize_product(product), status=status.HTTP_200_OK)
