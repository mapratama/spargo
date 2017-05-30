from spargo.api.response import ErrorResponse
from spargo.api.views import SessionAPIView
from spargo.apps.orders.models import Order
from spargo.apps.orders.utils import get_order_active
from spargo.core.serializers import serialize_order

from rest_framework import status
from rest_framework.response import Response

from .forms import (ItemCreationForm, OrderCreationForm, SentOfferingForm,
                    AcceptOfferingForm, PaymentCheckedForm, DeliverForm,
                    CompletedForm, CanceledForm)


class Preview(SessionAPIView):

    def post(self, request):
        order_data = request.data.get('order', {})
        items_data = request.data.get('items')

        total_price = 0
        for item in items_data:
            form = ItemCreationForm(data=item)
            if not form.is_valid():
                return ErrorResponse(form=form)

            product = form.cleaned_data['product']
            quantity = form.cleaned_data['quantity']
            price = product.price * quantity
            total_price = total_price + price

        delivery_fee = 15000

        order_form = OrderCreationForm(data=order_data)
        if order_form.is_valid():
            response = {
                'total_price': total_price,
                'delivery_fee': delivery_fee
            }

            return Response(response, status=status.HTTP_200_OK)
        return ErrorResponse(form=order_form)


class Create(SessionAPIView):

    def post(self, request):
        order_data = request.data.get('order', {})
        items_data = request.data.get('items')

        item_forms = []
        for item in items_data:
            form = ItemCreationForm(data=item)
            if not form.is_valid():
                return ErrorResponse(form=form)
            item_forms.append(form)

        order_form = OrderCreationForm(data=order_data)
        if order_form.is_valid():
            order = order_form.save(user=request.user)
            for form in item_forms:
                form.save(order=order)

            response = serialize_order(order)

            return Response(response, status=status.HTTP_200_OK)
        return ErrorResponse(form=order_form)


class Index(SessionAPIView):
    def get(self, request):
        orders = request.user.orders.is_active()
        response = [serialize_order(order) for order in orders]
        return Response(response, status=status.HTTP_200_OK)


class Dashboard(SessionAPIView):
    def get(self, request):
        user = request.user
        if user.is_superuser:
            response = {
                'orders': [serialize_order(order) for order in get_order_active()]
            }
        else:
            return ErrorResponse(
                error_description="You don't have privilages for access Dashboard order"
            )

        return Response(response, status=status.HTTP_200_OK)


class Details(SessionAPIView):
    def get(self, request, id):
        try:
            order = Order.objects.get(id=id)
        except Order.DoesNotExist:
            return ErrorResponse(error_description='Order Not Found')

        return Response(serialize_order(order), status=status.HTTP_200_OK)


class SentOffering(SessionAPIView):
    def post(self, request):
        form = SentOfferingForm(data=request.data)
        if form.is_valid():
            order = form.save()
            return Response(serialize_order(order), status=status.HTTP_200_OK)
        return ErrorResponse(form=form)


class AcceptOffering(SessionAPIView):
    def post(self, request):
        form = AcceptOfferingForm(user=request.user, data=request.data)
        if form.is_valid():
            order = form.save()
            return Response(serialize_order(order), status=status.HTTP_200_OK)
        return ErrorResponse(form=form)


class PaymentChecked(SessionAPIView):
    def post(self, request):
        form = PaymentCheckedForm(data=request.data)
        if form.is_valid():
            order = form.save(user=request.user)
            return Response(serialize_order(order), status=status.HTTP_200_OK)
        return ErrorResponse(form=form)


class Deliver(SessionAPIView):
    def post(self, request):
        form = DeliverForm(data=request.data)
        if form.is_valid():
            order = form.save()
            return Response(serialize_order(order), status=status.HTTP_200_OK)
        return ErrorResponse(form=form)


class Completed(SessionAPIView):
    def post(self, request):
        form = CompletedForm(user=request.user, data=request.data)
        if form.is_valid():
            order = form.save()
            return Response(serialize_order(order), status=status.HTTP_200_OK)
        return ErrorResponse(form=form)


class Canceled(SessionAPIView):
    def post(self, request):
        form = CanceledForm(user=request.user, data=request.data)
        if form.is_valid():
            order = form.save()
            return Response(serialize_order(order), status=status.HTTP_200_OK)
        return ErrorResponse(form=form)
