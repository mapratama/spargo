from spargo.apps.banks.models import Bank
from spargo.apps.banners.models import Banner
from spargo.apps.categories.models import Category
from spargo.apps.products.models import Product

from spargo.core.serializers import (serialize_user, serialize_category,
                                     serialize_banner, serialize_order,
                                     serialize_product, serialize_bank)


def success_response(user, session_key):
    banners = [serialize_banner(banner) for banner in Banner.objects.is_active()]
    categories = [serialize_category(category) for category in Category.objects.is_active()]
    products = [serialize_product(product) for product in Product.objects.is_active()]
    orders = [serialize_order(order) for order in user.orders.is_active()]
    banks = [serialize_bank(bank) for bank in Bank.objects.is_active()]

    response = {
        'session_key': session_key,
        'user': serialize_user(user),
        'banners': banners,
        'categories': categories,
        'products': products,
        'orders': orders,
        'banks': banks,
    }

    return response
