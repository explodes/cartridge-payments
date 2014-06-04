cartridge-payments
==================

**NOTE:** *Requires cartridge 0.8.2 or higher*
*The shop/checkout.html template has 3 blocks that are required. nav-buttons, before-form, and after-form.*

Cartridge multiple payment options module.

Features
-------------------------

This package lets you specify an optional Primary Payment Processor (in the normal cartridge way) and any number of extra processors. (ones that link out like Paypal Standard or Google Wallet ).

On the payment page the regular form shows up, if enabled, as well as buttons to submit form data out to the secondary payment providers.

Installation
-------------------------

Install the package by running the following command in your virtual environment:
    
    pip install cartridge-payments
    
Add the following minimum settings to your settings file:

    INSTALLED_APPS = (
	    # ...
	    "payments.multipayments",
	    # ...
	)
	
	TEMPLATE_CONTEXT_PROCESSORS = (
	    # ...
	    "payments.multipayments.context_processors.settings",
	    # ...
	)
    
    # USE or EXTEND the custom callback-uuid form
	SHOP_CHECKOUT_FORM_CLASS = 'payments.multipayments.forms.base.CallbackUUIDOrderForm'
	
	# Add the callback_uuid field to orders. This field is helpful for identifying
	# orders being checked out.
	EXTRA_MODEL_FIELDS = (
        # ...
	    (
	        "cartridge.shop.models.Order.callback_uuid",
	        "django.db.models.CharField",
	        (),
	        {"blank" : False, "max_length" : 36, 'default': 0},
	    ),
        # ...
	)


    # WHEN TRUE, Users will be able to submit payment using the regular paradigm
	# as well as the secondary payment processors.  WHEN FALSE the regular paradigm
	# will be hidden / disabled.
	PRIMARY_PAYMENT_PROCESSOR_IN_USE = True
	
	# These processors are forms to submit to remote URLs for processing.
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

Migrate Existing Database
-------------------------

	python manage.py schemamigration cartridge.shop --auto
	python manage.py migrate shop

PayPal Configuration
-------------------------

One built-in processor is for PayPal.
PayPal IPN is not implemented by default, but is supported by specifying the `PAYPAL_IPN_URL` setting.

Add PayPal as a secondary payment processor.

	SECONDARY_PAYMENT_PROCESSORS = (
        # ...
	    ('paypal', {
	        'name' : 'Pay With Pay-Pal',
	        'form' : 'payments.multipayments.forms.paypal.PaypalSubmissionForm'
	    }),
        # ...
    )
        
Configure PayPal
    
    # Currency type.
    PAYPAL_CURRENCY = "USD"
    
    # Business account email. Sandbox emails look like this.
	PAYPAL_BUSINESS = 'seller_XXXXXXXX_biz@example.com' 
    
    # Use this to enable https on return URLs.  This is strongly recommended! (Except for sandbox)
	PAYPAL_RETURN_WITH_HTTPS = True 
    
	# Function that returns args for `reverse`. 
    # URL is sent to PayPal as the for returning to a 'complete' landing page.
	PAYPAL_RETURN_URL = lambda cart, uuid, order_form: ('shop_complete', None, None)
    
	# Function that returns args for `reverse`. 
    # URL is sent to PayPal as the URL to callback to for PayPal IPN.
	# Set to None if you do not wish to use IPN.
	PAYPAL_IPN_URL = lambda cart, uuid, order_form: ('my_paypal_ipn', None, {'uuid' : uuid})
        
	# URL the secondary-payment-form is submitted to
    # Dev example
	PAYPAL_SUBMIT_URL = 'https://www.sandbox.paypal.com/cgi-bin/webscr'
    # Prod example
    PAYPAL_SUBMIT_URL = 'https://www.paypal.com/cgi-bin/webscr'

Google Wallet Configuration
-------------------------

Another built-in processor is for Google Wallet.
Google wallets callbacks are not implemented but are supported because `callback_uuid`'s are
sent to Google Wallet as `merchant-private-data`. 

Add Google Wallet as a secondary payment processor.

    SECONDARY_PAYMENT_PROCESSORS = (
        # ...
	    ('google', {
            'name' : 'Pay With Google Wallet',
	        'form' : 'payments.multipayments.forms.google.GoogleSubmissionForm'
	    }),
        # ...
    )
        
Configure Google Wallet
    
    # URL the secondary-payment-form is submitted to
    # Dev example
    GOOGLE_CHECKOUT_SUBMIT_URL = \
	    'https://sandbox.google.com/checkout/api/checkout/v2/checkoutForm/Merchant/<my-merchant-id>'
    # Prod example
    GOOGLE_CHECKOUT_SUBMIT_URL = \
	    'https://checkout.google.com/api/checkout/v2/checkout/Merchant/<my-merchant-id>'
