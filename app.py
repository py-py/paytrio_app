import hashlib
import os
import uuid

import requests
from flask import Flask, flash, render_template, request, redirect

from config import config
from currency import get_currencies

# load name of config in OS.ENVIRONMENT

config_name = os.getenv('APP_CONFIG') or 'default'

app = Flask(__name__)
app.config.from_object(config[config_name])
# config[config_name].init_app(app)


class InvoiceData:
    keys_required = []

    def __init__(self, data):
        from currency import get_currencies
        self.currency = next(c for c in get_currencies() if c.name == data['currency'].upper())
        self.invoice_id = str(uuid.uuid4()).replace('-', '')
        self.secret = app.config.get('SHOP_KEY')

        self._data = {'shop_id': app.config.get('SHOP_ID'),
                      'amount': data['amount'],
                      'description': data['description'],
                      'currency': self.currency.code,
                      'shop_invoice_id': self.invoice_id,
                      'payway': self.currency.payeer,
                      'url': self.currency.url,
                      }

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, update_data):
        self._data.update(update_data)

    def _contains_keys(self):
        return set(self.keys_required).issubset(set(self.data.keys()))

    def _make_sign(self):
        if self._contains_keys():
            sorted_key = sorted(self.keys_required)
            s = ':'.join(str(self.data[k]) for k in sorted_key) + self.secret
            return hashlib.md5(s.encode()).hexdigest()

    def sign(self):
        self.data.update({'sign': self._make_sign()})

    def fetch_data(self):
        try:
            r = requests.post(self.data['url'], json=self.invoice.data)
        except requests.exceptions.ConnectionError:
            # LOG: URL was not reached
            flash('{} is not valid'.format(self.URL))
        else:
            return r.json()
        return None



def validate_request_data(data):
    try:
        valid_amount = data.get('amount') if 1 < int(data.get('amount')) < 10000 else None
        valid_currency = data.get('currency') if data.get('currency') in (c.name for c in get_currencies()) else None
        valid_description = data.get('description') if len(data.get('description')) > 3 else None
    except ValueError:
        return False
    else:
        if valid_amount and valid_currency and valid_description:
            return True
    return False


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST' and validate_request_data(request.form):
        curr_form = request.form['currency']
        invoice = InvoiceData(request.form)

        if curr_form == 'USD':
            invoice.keys_required = ['amount', 'currency', 'shop_id', 'shop_invoice_id']
            invoice.sign()
            return render_template("usd_invoice.html", data=invoice.data)

        elif curr_form == 'EUR':
            invoice.keys_required = ['amount', 'currency', 'payway', 'shop_id', 'shop_invoice_id']
            invoice.sign()
            #fetch data
            json_data = invoice.fetch_data()
            return redirect(json_data['data']['data']['referer'])

    elif request.method == 'POST':
        # TODO: can add full flash about form's error
        flash('Form is not valid')

    return render_template("index.html",
                           currencies=get_currencies())


if __name__ == '__main__':
    app.run()
