from decimal import Decimal

from django import forms
from mezzanine.conf import settings

from payments.multipayments.forms import base
from payments.multipayments import const


class PaypalSubmissionForm(base.ExternalPaymentForm):

    invoice = forms.IntegerField(widget=forms.HiddenInput())
    first_name = forms.CharField(required=False, widget=forms.HiddenInput())
    last_name = forms.CharField(required=False, widget=forms.HiddenInput())
    email = forms.EmailField(required=False, widget=forms.HiddenInput())
    city = forms.CharField(required=False, widget=forms.HiddenInput())
    zip = forms.CharField(required=False, widget=forms.HiddenInput())
    country = forms.CharField(required=False, widget=forms.HiddenInput())
    amount = forms.DecimalField(widget=forms.HiddenInput())
    currency_code = forms.CharField(widget=forms.HiddenInput())
    notify_url = forms.CharField(required=False, widget=forms.HiddenInput())
    business = forms.EmailField(widget=forms.HiddenInput())
    cmd = forms.CharField(widget=forms.HiddenInput(), initial='_cart')
    upload = forms.CharField(widget=forms.HiddenInput(), initial='1')
    charset = forms.CharField(widget=forms.HiddenInput(), initial='utf-8')
    custom = forms.CharField(required=False, widget=forms.HiddenInput())

    def __init__(self, request, order_form, *args, **kwargs):

        super(PaypalSubmissionForm, self).__init__(*args, **kwargs)

        cart = request.cart
        self.order = self.get_or_create_order(request, order_form)

        form_value = lambda name, default: request.POST.get(\
                        'shipping_detail_%s' % name, default)

        shipping_type = request.session.get("shipping_type")
        shipping_total = request.session.get("shipping_total")

        tax_type = request.session.get("tax_type")
        tax_total = request.session.get("tax_total")

        cart_price = cart.total_price()
        ship_price = Decimal(str(shipping_total)).quantize(const.NEAREST_CENT)
        tax_price = Decimal(str(tax_total)).quantize(const.NEAREST_CENT)
        total_price = cart_price + \
            (ship_price if ship_price else Decimal('0')) + \
            (tax_price if tax_price else const.Decimal('0'))

        try:
            s_key = request.session.session_key
        except:
            # for Django 1.4 and above
            s_key = request.session._session_key

        # a keyword, haha :)
        self.fields['return'] = forms.CharField(widget=forms.HiddenInput())
        #paypal = get_backend_settings('paypal')
        #customer = payment.get_customer_data()
        self.fields['invoice'].initial = self.order.callback_uuid
        self.fields['first_name'].initial = form_value('first_name', '')
        self.fields['last_name'].initial = form_value('last_name', '')
        self.fields['email'].initial = form_value('email', '')
        self.fields['city'].initial = form_value('city', '')
        self.fields['country'].initial = form_value('country_iso', '')
        self.fields['zip'].initial = form_value('postal_code', '')
        self.fields['amount'].initial = total_price
        self.fields['currency_code'].initial = settings.PAYPAL_CURRENCY
        self.fields['business'].initial = settings.PAYPAL_BUSINESS
        self.fields['custom'].initial = ','.join([s_key, str(request.cart.pk)])

        i = 1
        if cart.has_items():
            for item in cart.items.all():
                rounded = item.unit_price.quantize(const.NEAREST_CENT)
                qty = int(item.quantity)
                self.add_line_item(i, item.description, rounded, qty)
                i += 1

        # Add shipping as a line item
        if shipping_type and shipping_total:
            self.add_line_item(i, shipping_type, shipping_total, 1)
            i += 1

        # Add tax as a line item
        if tax_type and tax_total:
            self.add_line_item(i, tax_type, tax_total, 1)
            i += 1

        self.fields['return'].initial = self.lambda_reverse(\
            settings.PAYPAL_RETURN_URL, cart, self.order.callback_uuid, \
            order_form)

        self.fields['notify_url'].initial = self.lambda_reverse(\
            settings.PAYPAL_IPN_URL, cart, self.order.callback_uuid, order_form)

    def add_line_item(self, number, name, amount, quantity):
        # FIELDS
        self.fields['item_name_%d' % number] = self._hidden_charfield()
        self.fields['amount_%d' % number] = self._hidden_charfield()
        self.fields['quantity_%d' % number] = self._hidden_charfield()
        # VALUES
        self.fields['item_name_%d' % number].initial = name
        self.fields['amount_%d' % number].initial = amount
        self.fields['quantity_%d' % number].initial = quantity

    def _hidden_charfield(self):
        return forms.CharField(widget=forms.HiddenInput())

    @property
    def action(self):
        return settings.PAYPAL_SUBMIT_URL
