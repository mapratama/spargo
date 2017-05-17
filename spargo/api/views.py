from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from django.views.decorators.csrf import csrf_exempt

from .authentication import (APISessionAuthentication, JSONSingleTokenAuthentication)
from .exceptions import APIError

from .parsers import JSONParser
from .permissions import IsSecure


class SpargoAPIView(APIView):
    permission_classes = (IsSecure,)
    authentication_classes = (JSONSingleTokenAuthentication,)

    renderer_classes = (JSONRenderer,)
    parser_classes = (JSONParser,)

    logging_key = None

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        # save this first before consumed by DRF-Request
        # Hit the method for API
        response = super(SpargoAPIView, self).dispatch(request, *args, **kwargs)

        return response

    def handle_exception(self, exc):
        """ Override the exception handler to handle APIError first
        """
        if isinstance(exc, APIError):
            return Response({'detail': exc.detail}, status=exc.status_code,
                            exception=True)
        return super(SpargoAPIView, self).handle_exception(exc)


class SessionAPIView(SpargoAPIView):

    authentication_classes = (JSONSingleTokenAuthentication, APISessionAuthentication)
