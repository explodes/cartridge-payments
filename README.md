cartridge-payments
==================

Cartridge multiple payment options module.

Features
-------------------------
This package lets you specify an optional Primary Payment Processor (in the normal cartridge way) and any number of extra processors. (ones that link out like Paypal Standard or Google Wallet ).

On the payment page the regular form shows up, if enabled, as well as buttons to submit form data out to the secondary payment providers.

Settings
-------------------------
The following settings can be found in payments/multipayments/template/settings.py and should be put in your settings.py file.

    ###################
    # PAYMENT OPTIONS #
    ###################

    # WHEN TRUE, Users will be able to submit payment using the regular paradigm
    # as well as the secondary payment processors.  WHEN FALSE the regular paradigm
    # will be hidden / disabled.
    PRIMARY_PAYMENT_PROCESSOR_IN_USE = True

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