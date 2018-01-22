from wtforms import Form
from wtforms import IntegerField, SelectField, StringField, SubmitField, HiddenField
from wtforms import validators

# TODO: import from currency
SELECTED_CURRENCIES = [('USD', 'USD'), ('EUR', 'EUR')]


class MainFormInvoice(Form):
    # sum max 1M
    amount = IntegerField('Amount', validators=[validators.NumberRange(min=0, max=1000000), validators.DataRequired()],
                          render_kw={"placeholder": "Input the sum of payment"})
    currency = SelectField('Currency', validators=[validators.DataRequired()],
                           choices=SELECTED_CURRENCIES)
    description = StringField('Description', validators=[validators.DataRequired()],
                              render_kw={"placeholder": "Input the aim's description"})
    submit = SubmitField('Submit')


class USDFormInvoice(Form):
    amount = HiddenField('Amount')
    currency = HiddenField('Currency')
    shop_id = HiddenField('Shop ID')
    sign = HiddenField('Sign')
    shop_invoice_id = HiddenField('Invoice ID')
    description = HiddenField('Description')
    submit = SubmitField('Submit')


class EURFormInvoice(Form):
    pass