# Invoice is created
LOG_INVOICE_CREATED = 'The invoice № "{shop_invoice_id}" was created by the shop № "{shop_id}". ' \
                      'Amount: "{amount}", description: "{description}", currency: "{currency}".'

# URL is not reached
LOG_ERROR_URL = '"{url}" is not reached. Please, check "{url}"'

# USDHandle
LOG_USDHANDLER_COMPLETED = 'The invoice № "{shop_invoice_id}" with currency: "{currency}" was handled. ' \
                           'The rendered template was sent to user.'

# EURHandle
LOG_EURHANDLER_COMPLETED = 'The invoice № "{shop_invoice_id}" with currency: "{currency}" was handled and sent to {url}'
LOG_EURHANDLER_RESPONSE_ERROR = 'The invoice № "{shop_invoice_id}" has an error. Error: '
