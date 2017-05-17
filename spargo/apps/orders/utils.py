from datetime import timedelta

from django.utils import timezone

from spargo.apps.orders.models import Order


def get_order_active(number_of_days=3):
    today = timezone.localtime(timezone.now())
    last_day = today - timedelta(days=number_of_days)
    orders = Order.objects.filter(created__gte=last_day.replace(hour=0, minute=0, second=0))\
        .select_related("user").order_by("created")

    return orders
