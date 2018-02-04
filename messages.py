# Invoice is created
LOG_INVOICE_CREATED = 'The invoice № "{shop_invoice_id}" was created by the shop № "{shop_id}". ' \
                      'Amount: "{amount}", description: "{description}", currency: "{currency}".'

# URL is not reached
LOG_ERROR_URL = '"{0}" is not reached. Please, check "{0}"'

# USDHandle
LOG_USDHANDLER_COMPLETED = 'The invoice № "{shop_invoice_id}" with currency: "{currency}" was handled. ' \
                           'The rendered template was sent to user.'

# EURHandle
LOG_EURHANDLER_COMPLETED = 'The invoice № "{shop_invoice_id}" with currency: "{currency}" was handled and sent to {0}'
LOG_EURHANDLER_RESPONSE_ERROR = 'The invoice № "{shop_invoice_id}" has an error. Error: {}.'
