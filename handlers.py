import hashlib

import requests
from flask import current_app, flash, redirect, render_template, url_for
from werkzeug.datastructures import ImmutableMultiDict

from messages import LOG_USDHANDLER_COMPLETED,LOG_INVOICE_CREATED, LOG_ERROR_URL, \
    LOG_EURHANDLER_COMPLETED, LOG_EURHANDLER_RESPONSE_ERROR


class Handle:
    URL = None
    keys_required = []

    def __init__(self, form_data):
        self.secret = current_app.config['SHOP_KEY']
        self.invoice = Invoice(form_data)
        # LOG: invoice was created
        current_app.logger.info(LOG_INVOICE_CREATED.format(**self.invoice.data))

    # check contains keys_required in invoice.data
    def contains_keys(self):
        return set(self.keys_required).issubset(set(self.invoice.data.keys()))

    # create the sign of required keys
    def make_sign(self):
        sorted_key = sorted(self.keys_required)
        s = ':'.join(str(self.invoice.data[k]) for k in sorted_key) + self.secret
        return hashlib.md5(s.encode()).hexdigest()


class USDHandle(Handle):
    URL = 'https://tip.pay-trio.com/en/'
    keys_required = ['amount', 'currency', 'shop_id', 'shop_invoice_id']

    def __init__(self, form_data):
        super().__init__(form_data)
        if self.contains_keys():
            self.invoice.sign(self.make_sign())
            # TODO: Verify do we need to make response manually (html form with hidden inputs) or js
            # create form according to task
            # self.form = USDFormInvoice(ImmutableMultiDict(self.invoice.data.items()))

    def make_response(self):
        current_app.logger.info(LOG_USDHANDLER_COMPLETED.format(**self.invoice.data))
        return render_template("usd_invoice.html", form=self.form, URL=self.URL)


class EURHandle(Handle):
    URL = 'https://central.pay-trio.com/invoice'
    keys_required = ['amount', 'currency', 'payway', 'shop_id', 'shop_invoice_id']

    def __init__(self, form_data):
        super().__init__(form_data)
        self.invoice.data.update({'payway': self.invoice.currency.payeer})
        if self.contains_keys():
            self.invoice.sign(self.make_sign())

    def fetch_data(self):
        try:
            r = requests.post(self.URL, json=self.invoice.data)
            return r.json()
        except requests.exceptions.ConnectionError:
            # LOG: URL was not reached
            current_app.logger.warning(LOG_ERROR_URL.format(self.URL))
            flash('{} is not valid'.format(self.URL))
            return None

    def make_response(self):
        # Got a result: None or Response
        json_response = self.fetch_data()
        if json_response:
            try:
                if json_response['result'] == 'ok':
                    json_data = json_response['data']
                else:
                    # LOG: a json's result has error
                    current_app.logger.warning(LOG_EURHANDLER_RESPONSE_ERROR.format(json_response['message'],
                                                                                    **self.invoice.data))
                    flash('EUR Payment has error {}'.format(json_response['message']))
                    return redirect(url_for('main.main_invoice'))
            except KeyError:
                # TODO: can be more detalize
                flash('Something went wrond :(')
                return redirect(url_for('main.main_invoice'))
            else:
                refer_url = json_data['data']['referer']
                # LOG: EURHandle is OK!
                current_app.logger.info(LOG_EURHANDLER_COMPLETED.format(self.URL, **self.invoice.data))
                return redirect(refer_url)
        return redirect(url_for('main.main_invoice'))