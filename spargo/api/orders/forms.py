from django import forms

from spargo.apps.orders.models import Order, Payment
from spargo.apps.products.models import Product
from spargo.core.notifications import (send_new_order_notification,
                                       send_bid_installation_order_notification,
                                       send_offering_notification,
                                       send_accept_offering_notification,
                                       send_payment_checked_notification,
                                       send_deliver_notification,
                                       send_completed_notification,
                                       send_canceled_notification)


class OrderCreationForm(forms.Form):
    address = forms.CharField()
    price = forms.FloatField()
    delivery_fee = forms.FloatField()
    weight = forms.FloatField()
    deliver_type = forms.TypedChoiceField(choices=Order.DELIVER_TYPE, coerce=int)
    with_installation = forms.BooleanField(initial=False, required=False)
    extra_data = forms.CharField(required=False)
    notes = forms.CharField(required=False)
    lat = forms.FloatField(required=False)
    long = forms.FloatField(required=False)

    def clean(self):
        cleaned_data = super(OrderCreationForm, self).clean()

        if self.errors:
            return cleaned_data

        deliver_type = cleaned_data['deliver_type']
        if deliver_type == Order.DELIVER_TYPE.spargo:
            if not cleaned_data['lat'] or not cleaned_data['long']:
                raise forms.ValidationError('Please fill your complete location')

    def save(self, user):
        with_installation = self.cleaned_data['with_installation']
        status = Order.STATUS.pending if with_installation else Order.STATUS.created
        order = Order.objects.create(
            user=user,
            price=self.cleaned_data['price'],
            status=status,
            with_installation=with_installation,
            delivery_fee=self.cleaned_data['delivery_fee'],
            deliver_type=self.cleaned_data['deliver_type'],
            weight=self.cleaned_data['weight'],
            extra_data=self.cleaned_data['extra_data'],
            address=self.cleaned_data['address'],
            lat=self.cleaned_data['lat'],
            long=self.cleaned_data['long'],
            notes=self.cleaned_data['notes']
        )

        if with_installation:
            send_bid_installation_order_notification()
        else:
            send_new_order_notification()

        return order


class ItemCreationForm(forms.Form):
    product = forms.ModelChoiceField(queryset=None)
    quantity = forms.IntegerField()
    notes = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super(ItemCreationForm, self).__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.is_active()

    def clean_product(self):
        product = self.cleaned_data['product']
        if product.stock == 0:
            raise forms.ValidationError('Stock %s is already empty' % product.name)

        return product

    def save(self, order, *args, **kwargs):
        product = self.cleaned_data['product']
        quantity = self.cleaned_data['quantity']
        notes = self.cleaned_data['notes']
        price = product.price * quantity
        item = order.items.create(
            product=product, quantity=quantity,
            price=price, notes=notes
        )

        product.stock = product.stock - quantity
        product.save(update_fields=['stock'])

        return item


class SentOfferingForm(forms.Form):

    order = forms.ModelChoiceField(
        queryset=Order.objects.filter(status=Order.STATUS.pending)
    )
    offering = forms.FloatField()

    def save(self):
        order = self.cleaned_data['order']
        order.installation_fee = self.cleaned_data['offering']
        order.status = Order.STATUS.installation_bid
        order.save(update_fields=['installation_fee', 'status'])

        send_offering_notification(order)

        return order


class AcceptOfferingForm(forms.Form):

    order = forms.ModelChoiceField(queryset=None)

    def __init__(self, user, *args, **kwargs):
        super(AcceptOfferingForm, self).__init__(*args, **kwargs)
        self.fields['order'].queryset = user.orders.filter(status=Order.STATUS.installation_bid)

    def save(self):
        order = self.cleaned_data['order']
        order.status = Order.STATUS.created
        order.save(update_fields=['status'])

        send_accept_offering_notification(order)

        return order


class PaymentCheckedForm(forms.Form):

    payment = forms.ModelChoiceField(
        queryset=Payment.objects.filter(status=Payment.STATUS.new)
    )
    status = forms.TypedChoiceField(choices=Payment.STATUS, coerce=int)

    def clean(self):
        cleaned_data = super(PaymentCheckedForm, self).clean()

        if self.errors:
            return cleaned_data

        payment = cleaned_data['payment']
        if payment.order.status != Order.STATUS.paid:
            raise forms.ValidationError('Sorry, status order already change to %s'
                                        % payment.order.get_status_display())

        status = cleaned_data['status']
        if status == Payment.STATUS.new:
            raise forms.ValidationError('Please select valid chooice')

    def save(self, user):
        payment = self.cleaned_data['payment']
        status = self.cleaned_data['status']
        payment.status = status
        payment.correction_by = user
        payment.save(update_fields=['status', 'correction_by'])

        order = payment.order
        if status == Payment.STATUS.accepted:
            order.status = Order.STATUS.payment_approved
            order.save(update_fields=['status'])

        send_payment_checked_notification(payment)

        return order


class DeliverForm(forms.Form):

    order = forms.ModelChoiceField(
        queryset=Order.objects.filter(status=Order.STATUS.payment_approved)
    )

    def save(self):
        order = self.cleaned_data['order']
        order.status = Order.STATUS.deliver
        order.save(update_fields=['status'])

        send_deliver_notification(order)

        return order


class CompletedForm(forms.Form):

    order = forms.ModelChoiceField(queryset=None)

    def __init__(self, user, *args, **kwargs):
        super(CompletedForm, self).__init__(*args, **kwargs)
        self.fields['order'].queryset = user.orders.filter(status=Order.STATUS.deliver)

    def save(self):
        order = self.cleaned_data['order']
        order.status = Order.STATUS.completed
        order.save(update_fields=['status'])

        send_completed_notification(order)

        return order


class CanceledForm(forms.Form):

    order = forms.ModelChoiceField(queryset=None)

    def __init__(self, user, *args, **kwargs):
        super(CanceledForm, self).__init__(*args, **kwargs)
        self.fields['order'].queryset = \
            user.orders.filter(status__in=[Order.STATUS.pending, Order.STATUS.created])

    def save(self):
        order = self.cleaned_data['order']
        order.status = Order.STATUS.canceled
        order.save(update_fields=['status'])

        for item in order.items.all():
            product = item.product
            product.stock = product.stock + item.quantity
            product.save(update_fields=['stock'])

        send_canceled_notification(order)

        return order
