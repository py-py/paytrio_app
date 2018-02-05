import os
import sys
import hashlib
import uuid
import requests
import logging
from logging.handlers import RotatingFileHandler

from flask import Flask, flash, render_template, request, redirect, url_for

from config import config
from currency import get_currencies
from messages import LOG_INVOICE_CREATED, LOG_ERROR_URL, LOG_USDHANDLER_COMPLETED, LOG_EURHANDLER_COMPLETED, \
    LOG_EURHANDLER_RESPONSE_ERROR

# load name of config in OS.ENVIRONMENT
config_name = os.getenv('APP_CONFIG') or 'default'

app = Flask(__name__)
app.config.from_object(config[config_name])


# TODO: disable a STANDART LOGGER
if 'DYNO' in os.environ:
    app.logger.addHandler(logging.StreamHandler(sys.stdout))
    app.logger.setLevel(logging.INFO)
else:
    handler = RotatingFileHandler('./log/paytrio_rotated.log')
    handler.setLevel(logging.INFO)
    handler.setFormatter(logging.Formatter('%(asctime)s : %(name)s : %(levelname)s : %(message)s'))
    app.logger.addHandler(handler)


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
            r = requests.post(self.data['url'], json=self.data)
        except requests.exceptions.ConnectionError as e:
            flash('{} is not valid'.format(self.data['url']))
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
        app.logger.info(LOG_INVOICE_CREATED.format(**invoice.data))

        if curr_form == 'USD':
            invoice.keys_required = ['amount', 'currency', 'shop_id', 'shop_invoice_id']
            invoice.sign()
            app.logger.info(LOG_USDHANDLER_COMPLETED.format(**invoice.data))
            return render_template("usd_invoice.html", data=invoice.data)

        elif curr_form == 'EUR':
            invoice.keys_required = ['amount', 'currency', 'payway', 'shop_id', 'shop_invoice_id']
            invoice.sign()
            json_data = invoice.fetch_data()
            if json_data is None:
                app.logger.info(LOG_ERROR_URL.format(**invoice.data))
                return redirect(url_for(index))
            if json_data.get('result') == 'ok':
                app.logger.info(LOG_EURHANDLER_COMPLETED.format(**invoice.data))
                return redirect(json_data['data']['data']['referer'])
            else:
                app.logger.info(LOG_EURHANDLER_RESPONSE_ERROR.format(**invoice.data) +
                                json_data.get('message', 'unreachable'))
                flash('EUR payment is not valid. There is an error: {}.'
                      .format(json_data.get('message', 'unreachable')))
    elif request.method == 'POST':
        flash('Form is not valid')

    return render_template("index.html",
                           currencies=get_currencies())


if __name__ == '__main__':
    app.run()
