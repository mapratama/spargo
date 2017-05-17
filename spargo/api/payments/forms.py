from spargo.apps.orders.models import Order, Payment
from spargo.core.notifications import send_new_payment_notification

from rest_framework import serializers


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = ("order", 'photo', 'bank', 'sender', "notes")

    def validate(self, validated_data):
        order = validated_data['order']

        if order.payments.filter(status=Payment.STATUS.new).exists():
            raise serializers.ValidationError(
                {'payment': 'Mohon maaf, kami masih sedang memproses pembayaran anda sebelumnya'})

        return validated_data

    def create(self, validated_data):
        payment = Payment.objects.create(**validated_data)

        order = payment.order
        order.status = Order.STATUS.paid
        order.save(update_fields=['status'])

        send_new_payment_notification(order)

        return order
