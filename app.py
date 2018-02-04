import os
from flask import Flask, flash, render_template, request
from config import config


# load name of config in OS.ENVIRONMENT
config_name = os.getenv('APP_CONFIG') or 'default'

app = Flask(__name__)
app.config.from_object(config[config_name])
config[config_name].init_app(app)


@app.route('/usd')
def usd_invoice():
    return render_template('usd_invoice.html')


def validate_request_data(data):
    # TODO: fix
    return True


@app.route('/', methods=["GET", "POST"])
def index():
    from currency import get_currencies

    if request.method == "POST" and validate_request_data(request.form):
        currency_handler = next(c.handler for c in get_currencies() if c.name == request.form.get('currency'))
        return currency_handler(request.form).make_response()
    else:
        # TODO: can add full flash about form's error
        flash('Form is not valid')

    return render_template("index.html",
                           currencies=get_currencies())

if __name__ == '__main__':
    app.run()
