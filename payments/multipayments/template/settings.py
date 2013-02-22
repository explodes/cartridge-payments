###################
# PAYMENT OPTIONS #
###################

# WHEN TRUE, Users will be able to submit payment using the regular paradigm
# as well as the secondary payment processors.  WHEN FALSE the regular paradigm
# will be hidden / disabled.
PRIMARY_PAYMENT_PROCESSOR_IN_USE = True

# These processors are forms to submit to remote URLs for processing. For
# example, PayPal Express or Google Wallet.
SECONDARY_PAYMENT_PROCESSORS = (
    ('payment-key1', {
        'name' : 'Button Name 1',
        'form' : 'dot.separarted.form.Class1'
    }),
    ('payment-key2', {
        'name' : 'Button Name 2',
        'form' : 'dot.separarted.form.Class2'
    })
)

# EXAMPLE SETTINGS:

SECONDARY_PAYMENT_PROCESSORS = (
    ('paypal', {
        'name' : 'Pay With Pay-Pal',
        'form' : 'payments.multipayments.forms.paypal.PaypalSubmissionForm'
    }),
    ('google', {
        'name' : 'Pay With Google Wallet',
        'form' : 'payments.multipayments.forms.google.GoogleSubmissionForm'
    })
)

## PaypalSubmissionForm requires:
PAYPAL_CURRENCY = "USD"
PAYPAL_BUSINESS = 'seller_XXXXXXXX_biz@example.com'  # Sandbox generated business email
PAYPAL_RETURN_WITH_HTTPS = False  # Return URL
PAYPAL_RETURN_URL = lambda cart, uuid, order_form: ('shop_complete', None, None)  # Function that returns args for reverse. Generated URL is URL for returning landing page.
PAYPAL_IPN_URL = lambda cart, uuid, order_form: ('payment:paypal_ipn', None, {'uuid' : uuid})  # Function that returns args for reverse. Generated URL is URL for PayPal IPN.
PAYPAL_SUBMIT_URL = 'https://www.sandbox.paypal.com/cgi-bin/webscr'  # Dev url

## GoogleSubmissionForm requires:
GOOGLE_CHECKOUT_SUBMIT_URL = 'https://sandbox.google.com/checkout/api/checkout/v2/checkoutForm/Merchant/<my-merchant-id>'  # Sandbox URL
