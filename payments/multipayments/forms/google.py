from cartridge.shop import models as shop
from django import forms
from mezzanine.conf import settings

from payments.multipayments.forms import const



class GoogleSubmissionForm(forms.Form):

    charset = forms.CharField(required=True, widget=forms.HiddenInput())  # __charset__

    def __init__(self, request, order_form, *args, **kwargs):

        super(GoogleSubmissionForm, self).__init__(*args, **kwargs)

        # Form fields renaming
        self.fields['__charset__'] = self.fields.pop('charset')
        self.fields['__charset__'].initial = 'utf8'


        cart = request.cart
        uuid = request.session['order']['callback_uuid']
        self.create_order(request, uuid, order_form)
        shipping_type = request.session.get("shipping_type")
        shipping_total = request.session.get("shipping_total")

        i = 1
        if cart.has_items():
            for item in cart.items.all():
                self.add_line_item(i, item.description, item.total_price.quantize(const.NEAREST_CENT), int(item.quantity))
                i += 1


        if shipping_type and shipping_total:
            self.add_line_item(i, shipping_type, shipping_total, 1)


    def add_line_item(self, number, name, amount, quantity, description=''):
        # FIELDS
        self.fields['item_name_%d' % number] = forms.CharField(widget=forms.HiddenInput())
        self.fields['item_price_%d' % number] = forms.DecimalField(widget=forms.HiddenInput())
        self.fields['item_quantity_%d' % number] = forms.IntegerField(widget=forms.HiddenInput())
        self.fields['item_description_%d' % number] = forms.IntegerField(widget=forms.HiddenInput())
        # VALUES
        self.fields['item_name_%d' % number].initial = name
        self.fields['item_price_%d' % number].initial = amount
        self.fields['item_quantity_%d' % number].initial = quantity
        self.fields['item_description_%d' % number].initial = description

    @property
    def action(self):
        return settings.GOOGLE_CHECKOUT_SUBMIT_URL

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
