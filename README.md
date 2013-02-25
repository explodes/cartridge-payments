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
	
	# USE or EXTEND the custom callback-uuid form
	SHOP_CHECKOUT_FORM_CLASS = \
	    'payments.multipayments.forms.base.CallbackUUIDOrderForm'
	
	# Add the callback_uuid field to orders. This field is helpful for identifying
	# orders being checked out.
	EXTRA_MODEL_FIELDS = (
	    (
	        "cartridge.shop.models.Order.callback_uuid",
	        "django.db.models.CharField",
	        (),
	        {"blank" : False, "max_length" : 36},
	    ),
	)
	
	
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
	
	## PaypalSubmissionForm requires: ##
	PAYPAL_CURRENCY = "USD"
	# Sandbox generated business email
	PAYPAL_BUSINESS = 'seller_XXXXXXXX_biz@example.com'
	# Return URL
	PAYPAL_RETURN_WITH_HTTPS = False
	# Function that returns args for reverse. Generated URL is URL for returning
	# landing page.  For best results, use callback_uuid in the URL
	PAYPAL_RETURN_URL = \
	    lambda cart, uuid, order_form: ('shop_complete', None, None)
	# Function that returns args for reverse. Generated URL is URL for PayPal IPN.
	PAYPAL_IPN_URL = \
	    lambda cart, uuid, order_form: ('my_paypal_ipn', None, {'uuid' : uuid})
	# Dev url
	PAYPAL_SUBMIT_URL = 'https://www.sandbox.paypal.com/cgi-bin/webscr'
	
	## GoogleSubmissionForm requires:
	# Sandbox submission endpoint
	GOOGLE_CHECKOUT_SUBMIT_URL = \
	    'https://sandbox.google.com/checkout/api/checkout/v2/checkoutForm/Merchant/<my-merchant-id>'
	# If you specify a callback-URL in your wallet settings, make use of
	# callback_uuid as merchant-private-data
