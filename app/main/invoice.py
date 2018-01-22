import random
import string
from flask import current_app


class Invoice:
    failed_url = 'http://tip.pay-trio.com/failed/'
    success_url = 'http://tip.pay-trio.com/success/'

    def __init__(self, form_data):
        from app.main.currency import get_currencies
        self.currency = next(c for c in get_currencies() if c.name.upper() == form_data['currency'].upper())

        self._data = {'shop_id': current_app.config['SHOP_ID'],
                      'amount': form_data['amount'],
                      'description': form_data['description'],
                      'currency': self.currency.code,
                      'shop_invoice_id': self.make_invoice_id(),
                      }

    @staticmethod
    def make_invoice_id():
        return ''.join(random.choice(string.digits + string.ascii_lowercase) for _ in range(32))

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, update_data):
        self._data.update(update_data)

    def sign(self, key):
        self.data.update({'sign': key})
