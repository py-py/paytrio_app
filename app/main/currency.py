from .handlers import USDHandle, EURHandle


class USDCurrency:
    name = 'USD'
    code = 840
    handler = USDHandle
    payeer = 'card_usd'


class EURCurrency:
    name = 'EUR'
    code = 978
    handler = EURHandle
    payeer = 'payeer_eur'


def get_currencies():
    return [USDCurrency, EURCurrency]

