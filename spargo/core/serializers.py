import calendar

from django.conf import settings


def serialize_user(user):
    return {
        'id': user.id,
        'email': user.email,
        'name': user.name,
        'mobile_number': user.mobile_number,
        'gender': user.gender,
        'birthday': user.birthday.isoformat() if user.birthday else None,
    }


def serialize_banner(banner):
    photo_url = settings.HOST + banner.photo.thumbnails.get('size_600x600').url \
        if banner.photo else None

    return {
        'id': banner.id,
        'photo_url': photo_url,
        'is_active': banner.is_active,
    }


def serialize_jne(jne):
    return {
        'id': jne.id,
        'code': jne.code,
        'region': jne.region,
        'regular_cost': jne.regular_cost,
        'regular_estimated': jne.regular_estimated if jne.regular_estimated else 0,
        'oke_cost': jne.oke_cost if jne.oke_cost else 0,
        'oke_estimated': jne.oke_estimated if jne.oke_estimated else 0,
        'yes_cost': jne.yes_cost if jne.yes_cost else 0,
        'yes_estimated': jne.yes_estimated if jne.yes_estimated else 0,
    }


def serialize_j_and_t(j_and_t):
    return {
        'id': j_and_t.id,
        'code': j_and_t.code,
        'city': j_and_t.city,
        'cost': j_and_t.cost,
    }


def serialize_bank(bank):
    photo_url = settings.HOST + bank.photo.thumbnails.get('size_400').url \
        if bank.photo else None

    return {
        'id': bank.id,
        'name': bank.name,
        'account_number': bank.account_number,
        'account_name': bank.account_name,
        'photo_url': photo_url,
        'is_active': bank.is_active,
    }


def serialize_subtype(subtype):
    photo_url = settings.HOST + subtype.photo.thumbnails.get('size_600x300').url \
        if subtype.photo else None

    return {
        'id': subtype.id,
        'name': subtype.name,
        'description': subtype.description if subtype.description else None,
        'photo_url': photo_url,
        'is_active': subtype.is_active,
        'type': serialize_type(subtype.type)
    }


def serialize_type(type):
    photo_url = settings.HOST + type.photo.thumbnails.get('size_600x300').url \
        if type.photo else None

    return {
        'id': type.id,
        'name': type.name,
        'description': type.description if type.description else None,
        'photo_url': photo_url,
        'is_active': type.is_active,
    }


def serialize_photo(photo):
    photo_url = settings.HOST + photo.photo.thumbnails.get('size_600x400').url \
        if photo.photo else None

    return {
        'id': photo.id,
        'name': photo.name,
        'photo_url': photo_url,
        'is_active': photo.is_active,
    }


def serialize_category(category):
    photo_url = settings.HOST + category.photo.thumbnails.get('size_400').url \
        if category.photo else None

    return {
        'id': category.id,
        'name': category.name,
        'models': [serialize_model(model) for model in category.model.all()],
        'description': category.description if category.description else None,
        'photo_url': photo_url,
        'is_active': category.is_active,
    }


def serialize_model(model):
    photo_url = settings.HOST + model.photo.thumbnails.get('size_600x300').url \
        if model.photo else None

    return {
        'id': model.id,
        'name': model.name,
        'description': model.description if model.description else None,
        'photo_url': photo_url,
        'is_active': model.is_active,
    }


def serialize_product(product):

    return {
        'id': product.id,
        'name': product.name,
        'subtype': serialize_subtype(product.subtype_product),
        'models': [serialize_model(model) for model in product.model.all()],
        'photos': [serialize_photo(photo) for photo in product.photos.is_active()],
        'colour': product.colour if product.colour else '-',
        'weight': product.weight,
        'dimension': product.dimension if product.dimension else '-',
        'material': product.material if product.material else '-',
        'condition': product.get_condition_display(),
        'description': product.description if product.description else '-',
        'price': product.price,
        'stock': product.stock,
        'is_active': product.is_active,
    }


def serialize_order(order):

    return {
        'id': order.id,
        'user': serialize_user(order.user),
        'invoice_number': order.invoice_number,
        'code': order.code,
        'status': order.status,
        'deliver_type': order.deliver_type,
        'created': calendar.timegm(order.created.utctimetuple()),
        'price': order.price,
        'weight': order.weight,
        'with_installation': order.with_installation,
        'installation_fee': order.installation_fee,
        'delivery_fee': order.delivery_fee,
        'delivery_id': order.delivery_id if order.delivery_id else None,
        'address': order.address,
        'extra_data': order.extra_data if order.extra_data else None,
        'lat': order.lat if order.lat else None,
        'lang': order.long if order.long else None,
        'notes': order.notes if order.notes else '-',
        'items': [serialize_item(item) for item in order.items.all()],
        'payment': (serialize_payment(order.payments.last())
                    if order.payments.last() else None),
    }


def serialize_item(item):
    return {
        'id': item.id,
        'product': serialize_product(item.product),
        'quantity': item.quantity,
        'price': item.price,
        'notes': item.notes if item.notes else '-',
    }


def serialize_payment(payment):
    photo_url = settings.HOST + payment.photo.thumbnails.get('size_400x600').url \
        if payment.photo else None

    return {
        'id': payment.id,
        'sender': payment.sender,
        'status': payment.status,
        'bank': serialize_bank(payment.bank),
        'created': calendar.timegm(payment.created.utctimetuple()),
        'notes': payment.notes if payment.notes else '-',
        'photo_url': photo_url,
    }
