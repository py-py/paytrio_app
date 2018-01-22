from flask import flash
from flask import render_template, request

from app.main import main
from app.main.currency import get_currencies
from app.main.forms import MainFormInvoice


@main.route('/', methods=["GET", "POST"])
def main_invoice():
    form = MainFormInvoice(request.form)
    if form.validate():
        currency_handler = next(c.handler for c in get_currencies() if c.name == form.currency.data)
        return currency_handler(form.data).make_response()
    if request.method == 'POST':
        # TODO: can add full flash about error of attribute of form
        flash('Form is not valid')
    return render_template("main_invoice.html", form=form)
