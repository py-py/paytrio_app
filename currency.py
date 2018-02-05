class USDCurrency:
    name = 'USD'
    code = 840
    payeer = 'card_usd'
    url = 'https://tip.pay-trio.com/en/'


class EURCurrency:
    name = 'EUR'
    code = 978
    payeer = 'payeer_eur'
    url = 'https://central.pay-trio.com/invoice'


def get_currencies():
    return [USDCurrency, EURCurrency]
