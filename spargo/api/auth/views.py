from spargo.api.response import ErrorResponse
from spargo.api.views import SpargoAPIView, SessionAPIView
from spargo.apps.orders.utils import get_order_active
from spargo.core.utils import force_login
from spargo.core.serializers import serialize_order, serialize_user

from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm

from rest_framework import status
from rest_framework.response import Response

from .forms import APIRegistrationForm, PasswordResetForm
from .utils import success_response


class Login(SpargoAPIView):

    def post(self, request):
        form = AuthenticationForm(data=request.data)
        if form.is_valid():
            login(request, form.get_user())
            user = request.user

            push_notification_key = request.data.get('push_notification_key')
            if push_notification_key:
                user.push_notification_key = push_notification_key
                user.save(update_fields=['push_notification_key'])

            if user.is_superuser:
                response = {
                    'orders': [serialize_order(order) for order in get_order_active()],
                    'user': serialize_user(user),
                    'session_key': request.session.session_key
                }
            else:
                response = success_response(user, request.session.session_key)

            return Response(response, status=status.HTTP_200_OK)
        return ErrorResponse(form=form)


class Register(SpargoAPIView):

    def post(self, request):
        form = APIRegistrationForm(data=request.data)
        if form.is_valid():
            user = form.save()
            force_login(request, user)
            request.session.create()
            return Response(success_response(user, request.session.session_key),
                            status=status.HTTP_200_OK)
        return ErrorResponse(form=form)


class Logout(SessionAPIView):

    def post(self, request):
        logout(request)
        return Response({'status': 'ok'}, status=status.HTTP_200_OK)


class NotificationUpdate(SessionAPIView):

    def post(self, request):
        user = request.user
        user.gcm_key = request.data['gcm_key']
        user.save()

        return Response({'status': 'ok'}, status=status.HTTP_200_OK)


class ChangePassword(SessionAPIView):

    def post(self, request):
        form = PasswordChangeForm(data=request.data, user=request.user)
        if form.is_valid():
            form.save()
            return Response({'status': 'ok'}, status=status.HTTP_200_OK)
        return ErrorResponse(form=form)


class PasswordReset(SpargoAPIView):

    def post(self, request):
        form = PasswordResetForm(request.data)
        if form.is_valid():
            form.save()
            return Response({'status': 'ok'}, status=status.HTTP_200_OK)

        return ErrorResponse(form=form)
