import django_rq
from django.conf import settings

from gcm import GCM
from gcm.gcm import GCMInvalidRegistrationException, GCMNotRegisteredException

from spargo.apps.users.models import User
from spargo.apps.orders.models import Payment


def send_notification(user, data, async=True):
    gcm = GCM(settings.GOOGLE_API_KEY)

    if not user.push_notification_key:
        return

    kwargs = {
        "data": data,
        "registration_ids": [user.push_notification_key],
    }

    try:
        if async:
            django_rq.enqueue(gcm.json_request, **kwargs)
        else:
            gcm.json_request(**kwargs)
    except (GCMInvalidRegistrationException, GCMNotRegisteredException):
        return


def send_new_order_notification():
    users = User.objects.filter(is_active=True, is_superuser=True)
    for user in users:
        notification_data = {
            'title': 'Order baru',
            'body': 'Terdapat order baru masuk, silahkan reload data order di dalam dashboard',
            'action': 'sync_order',
        }
        send_notification(user, notification_data)


def send_bid_installation_order_notification():
    users = User.objects.filter(is_active=True, is_superuser=True)
    for user in users:
        notification_data = {
            'title': 'Permintaan order dengan biaya pemasangan',
            'body': ('Terdapat order baru masuk dengan memerlukan biaya pemasangan. '
                     'Silahkan input biaya pemasangan kepada user.'),
            'action': 'sync_order',
        }
        send_notification(user, notification_data)


def send_offering_notification(order):
    notification_data = {
        'title': 'Penawaran biaya pemasangan',
        'body': 'SPARGO menawarkan biaya pemasangan sebesar %s untuk order %s.'
                % (order.installation_fee, order.invoice_number),
        'action': 'sync_order_details',
        'extra_data': order.id
    }
    send_notification(order.user, notification_data)


def send_accept_offering_notification(order):
    users = User.objects.filter(is_active=True, is_superuser=True)
    for user in users:
        notification_data = {
            'title': 'Penawaran biaya pemasangan disetujui',
            'body': ('Customer untuk order %s menyetujui biaya pemasangan. '
                     'Silahkan reload data order di dalam dashboard') % order.invoice_number,
            'action': 'sync_order',
        }
        send_notification(user, notification_data)


def send_new_payment_notification(order):
    users = User.objects.filter(is_active=True, is_superuser=True)
    for user in users:
        notification_data = {
            'title': 'Order %s telah melakukan pembayaran' % order.invoice_number,
            'body': ('Customer untuk order %s telah melakukan pembayaran. '
                     'Silahkan konfirmasi pembayaran tersebut') % order.invoice_number,
            'action': 'sync_order',
        }
        send_notification(user, notification_data)


def send_payment_checked_notification(payment):
    order = payment.order
    if payment.status == Payment.STATUS.accepted:
        title = 'Pembayaran disetujui'
        body = ('Pembayaran untuk pesanan %s telah diterima, '
                'Terima kasih telah berbelanja di SPARGO') % order.invoice_number
    else:
        title = 'Pembayaran ditolak'
        body = ('Pembayaran untuk pesanan %s ditolak, '
                'Silahkan menghubungi contact center SPARGO') % order.invoice_number

    notification_data = {
        'title': title,
        'body': body,
        'action': 'sync_order_details',
        'extra_data': order.id
    }
    send_notification(order.user, notification_data)


def send_deliver_notification(order):
    notification_data = {
        'title': 'Barang telah dikirim',
        'body': 'Barang untuk order %s telah dikirim menuju %s'
                % (order.invoice_number, order.address),
        'action': 'sync_order_details',
        'extra_data': order.id
    }
    send_notification(order.user, notification_data)


def send_completed_notification(order):
    users = User.objects.filter(is_active=True, is_superuser=True)
    for user in users:
        notification_data = {
            'title': 'Barang telah diterima customer',
            'body': 'Barang untuk order %s telah diterima customer'
                    % order.invoice_number,
            'action': 'sync_order',
        }
        send_notification(user, notification_data)


def send_canceled_notification(order):
    users = User.objects.filter(is_active=True, is_superuser=True)
    for user in users:
        notification_data = {
            'title': 'Order %s telah dibatalkan' % order.invoice_number,
            'body': 'Order %s telah dibatalkan oleh customer'
                    % order.invoice_number,
            'action': 'sync_order',
        }
        send_notification(user, notification_data)
