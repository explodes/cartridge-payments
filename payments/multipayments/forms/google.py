from django import forms
from mezzanine.conf import settings

from payments.multipayments.forms import base
from payments.multipayments import const


class GoogleSubmissionForm(base.ExternalPaymentForm):

    # Override the name django gives the fields
    FIELD_NAME_MAPPING = {
        'charset' : '__charset__',
        'private_data' : 'shopping-cart.merchant-private-data',
    }

    charset = forms.CharField(required=True, widget=forms.HiddenInput())
    private_data = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, request, order_form, *args, **kwargs):

        super(GoogleSubmissionForm, self).__init__(*args, **kwargs)

        self.order = self.get_or_create_order(request, order_form)

        self.fields['charset'].initial = 'utf8'
        self.fields['private_data'].initial = self.order.callback_uuid

        cart = request.cart

        i = 1
        if cart.has_items():
            for item in cart.items.all():
                rounded = item.total_price.quantize(const.NEAREST_CENT)
                qty = int(item.quantity)
                self.add_line_item(i, item.description, rounded, qty)
                i += 1

    def add_line_item(self, number, name, amount, quantity, description=''):
        # FIELDS
        self.fields['item_name_%d' % number] = self._hidden_charfield()
        self.fields['item_price_%d' % number] = self._hidden_charfield()
        self.fields['item_quantity_%d' % number] = self._hidden_charfield()
        self.fields['item_description_%d' % number] = self._hidden_charfield()
        # VALUES
        self.fields['item_name_%d' % number].initial = name
        self.fields['item_price_%d' % number].initial = amount
        self.fields['item_quantity_%d' % number].initial = quantity
        self.fields['item_description_%d' % number].initial = description

    def _hidden_charfield(self):
        return forms.CharField(widget=forms.HiddenInput())

    @property
    def action(self):
        return settings.GOOGLE_CHECKOUT_SUBMIT_URL

    def add_prefix(self, field_name):
        # look up field name; return original if not found
        field_name = self.FIELD_NAME_MAPPING.get(field_name, field_name)
        return super(GoogleSubmissionForm, self).add_prefix(field_name)
