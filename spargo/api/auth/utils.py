from spargo.apps.banks.models import Bank
from spargo.apps.banners.models import Banner
from spargo.apps.categories.models import Category
from spargo.apps.jne.models import JNE
from spargo.apps.j_and_t.models import JAndT
from spargo.apps.products.models import Product

from spargo.core.serializers import (serialize_user, serialize_category,
                                     serialize_banner, serialize_order,
                                     serialize_product, serialize_bank,
                                     serialize_jne, serialize_j_and_t)


def success_response(user, session_key):
    banners = [serialize_banner(banner) for banner in Banner.objects.is_active()]
    categories = [serialize_category(category) for category in Category.objects.is_active()]
    products = [serialize_product(product) for product in Product.objects.is_active()]
    orders = [serialize_order(order) for order in user.orders.all()]
    banks = [serialize_bank(bank) for bank in Bank.objects.is_active()]
    jne = [serialize_jne(jne) for jne in JNE.objects.all()]
    j_and_t = [serialize_j_and_t(j_and_t) for j_and_t in JAndT.objects.all()]

    response = {
        'session_key': session_key,
        'user': serialize_user(user),
        'banners': banners,
        'categories': categories,
        'products': products,
        'orders': orders,
        'banks': banks,
        'jne': jne,
        'j_and_t': j_and_t,
    }

    return response
