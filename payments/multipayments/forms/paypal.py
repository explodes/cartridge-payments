from decimal import Decimal

from cartridge.shop import models as shop
from django import forms
from django.contrib.sites import models as sites
from django.core.urlresolvers import reverse
from mezzanine.conf import settings

from payments.multipayments.forms import const


class PaypalSubmissionForm(forms.Form):

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

    def __init__(self, request, order_form, *args, **kwargs):

        super(PaypalSubmissionForm, self).__init__(*args, **kwargs)

        cart = request.cart

        uuid = request.session['order']['callback_uuid']

        form_value = lambda name, default: request.POST.get('shipping_detail_%s' % name, default)

        self.create_order(request, uuid, order_form)

        shipping_type = request.session.get("shipping_type")
        shipping_total = request.session.get("shipping_total")

        cart_price = cart.total_price()
        shipping_price = Decimal(str(shipping_total)).quantize(const.NEAREST_CENT)
        total_price = cart_price + (shipping_price if shipping_price else Decimal('0'))

        # a keyword, haha :)
        self.fields['return'] = forms.CharField(widget=forms.HiddenInput())
        #paypal = get_backend_settings('paypal')
        #customer = payment.get_customer_data()
        self.fields['invoice'].initial = uuid
        self.fields['first_name'].initial = form_value('first_name', '')
        self.fields['last_name'].initial = form_value('last_name', '')
        self.fields['email'].initial = form_value('email', '')
        self.fields['city'].initial = form_value('city', '')
        self.fields['country'].initial = form_value('country_iso', '')
        self.fields['zip'].initial = form_value('postal_code', '')
        self.fields['amount'].initial = total_price
        self.fields['currency_code'].initial = settings.PAYPAL_CURRENCY
        self.fields['business'].initial = settings.PAYPAL_BUSINESS

        i = 1
        if cart.has_items():
            for item in cart.items.all():
                self.add_line_item(i, item.description, item.total_price.quantize(const.NEAREST_CENT), int(item.quantity))
                i += 1

        if shipping_type and shipping_total:
            # Add shipping + tax as a line item
            self.add_line_item(i, shipping_type, shipping_total, 1)

        protocol = 'https' if settings.PAYPAL_RETURN_WITH_HTTPS else 'http'
        domain = sites.Site.objects.get_current().domain

        base_url = '%s://%s' % (protocol, domain)

        self.fields['return'].initial = base_url + self.lambda_reverse(settings.PAYPAL_RETURN_URL, cart, uuid, order_form)
        self.fields['notify_url'].initial = base_url + self.lambda_reverse(settings.PAYPAL_IPN_URL, cart, uuid, order_form)

    def lambda_reverse(self, func, cart, uuid, order_form):

        view, args, kwargs = func(cart, uuid, order_form)
        return reverse(view, args=args, kwargs=kwargs)


    def add_line_item(self, number, name, amount, quantity):
        # FIELDS
        self.fields['item_name_%d' % number] = forms.CharField(widget=forms.HiddenInput())
        self.fields['amount_%d' % number] = forms.DecimalField(widget=forms.HiddenInput())
        self.fields['quantity_%d' % number] = forms.IntegerField(widget=forms.HiddenInput())
        # VALUES
        self.fields['item_name_%d' % number].initial = name
        self.fields['amount_%d' % number].initial = amount
        self.fields['quantity_%d' % number].initial = quantity

    @property
    def action(self):
        return settings.PAYPAL_SUBMIT_URL

    def clean(self, *args, **kwargs):
        raise NotImplementedError("This form is not intended to be validated here.")

    def create_order(self, request, uuid, order_form):
        try:
            order = shop.Order.objects.get(callback_uuid=uuid)
        except shop.Order.DoesNotExist:
            order = order_form.save(commit=False)
            order.setup(request)
            session_order = request.session['order']
            for key in order_form.fields.keys():
                if hasattr(order, key):
                    setattr(order, key, session_order[key])
            order.transaction_id = uuid
            order.save()
        return order
