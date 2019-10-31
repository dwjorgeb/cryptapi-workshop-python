import requests
import string
import random


CRYPTAPI_URL = "https://cryptapi.io/api/"


COINS = (
    ('btc', 'Bitcoin'),
    ('eth', 'Ethereum'),
    ('bch', 'Bitcoin Cash'),
    ('ltc', 'Litecoin'),
    ('iota', 'IOTA'),
    ('xmr', 'Monero'),
)


STATUS = (
    ('created', _('Created')),
    ('pending', _('Pending')),
    ('insufficient', _('Payment Insufficient')),
    ('received', _('Received')),
    ('done', _('Done')),
)


COIN_MULTIPLIERS = {
    'btc': 100000000,
    'bch': 100000000,
    'ltc': 100000000,
    'eth': 1000000000000000000,
    'iota': 1000000,
    'xmr': 1000000000000,
}


def generate_nonce(length=32):

    # Not cryptographically secure, but good enough for generating nonces

    sequence = string.ascii_letters + string.digits

    return ''.join([random.choice(sequence) for i in range(length)])


def build_callback_url(base_url, params):
    base_request = requests.Request(
        url=base_url,
        params=params
    ).prepare()

    return base_request.url


def process_request(coin, endpoint='create', params=None):

    if coin not in [c[0] for c in COINS]:
        raise Exception('Unknown coin selected')

    response = requests.get(
        url="{base_url}{coin}/{endpoint}".format(
            base_url=CRYPTAPI_URL,
            coin=coin,
            endpoint=endpoint,
        ),
        params=params
    )

    return response


def main():
    my_order_id = 1234
    nonce = generate_nonce()
    callback_base_url = 'http://webhook.site/7ed2757f-ae67-49eb-a816-9615680871e3'  # Add your own here
    my_btc_address = '1PE5U4temq1rFzseHHGE2L8smwHCyRbkx3'

    callback_url = build_callback_url(callback_base_url, {'order_id': my_order_id, 'nonce': nonce})
    params = {
        'callback': callback_url,
        'address': my_btc_address,
        'pending': 1,
    }

    response = process_request(coin='btc', endpoint='create', params=params)

    if response.status_code == 200:
        response_json = response.json()

        if response_json['status'] == 'success':
            payment_address = response_json['address_in']

            # Show the address to your customer or create a QR Code with it.


