from uuid import uuid4

from django import forms
from django.contrib.sites import models as sites
from django.core.urlresolvers import reverse
from cartridge.shop import checkout
from cartridge.shop import forms as shopforms
from cartridge.shop import models as shop
from mezzanine.conf import settings


class CallbackUUIDOrderForm(shopforms.OrderForm):

    callback_uuid = forms.CharField(max_length=36, min_length=36,
                                    widget=forms.HiddenInput(), initial=uuid4)

    def __init__(self, request, step, *args, **kwargs):
        # Set the callback_uuid to something new
        initial = kwargs.get('initial', {})
        is_first_step = step == checkout.CHECKOUT_STEP_FIRST
        
        if is_first_step or 'callback_uuid' not in initial:
            while True:
                callback_uuid = uuid4()
                count = shop.Order.objects.filter(callback_uuid=callback_uuid) \
                    .count()
                if not count:
                    break
            initial['callback_uuid'] = callback_uuid
        super(CallbackUUIDOrderForm, self).__init__(request, step, *args,
                                                     **kwargs)


class ExternalPaymentForm(forms.Form):

    def clean(self, *args, **kwargs):
        raise NotImplementedError("This form is not intended to be validated.")

    def get_or_create_order(self, request, order_form):
        '''
        Create an order from a uuid
        '''
        session_order = request.session.get('order', {})
        uuid = session_order.get('callback_uuid')

        try:
            order = shop.Order.objects.get(callback_uuid=uuid)
        except shop.Order.DoesNotExist:
            order = order_form.save(commit=False)
            order.setup(request)
            for key in order_form.fields.keys():
                if hasattr(order, key) and key in session_order:
                    setattr(order, key, session_order[key])
            order.transaction_id = uuid
            order.save()
        return order

    def lambda_reverse(self, func, cart, uuid, order_form):
        '''
        Return a url constructed from a lambda function in the format of:
        lambda cart, uuid, order_form
        '''
        if func:
            protocol = 'https' if settings.PAYPAL_RETURN_WITH_HTTPS else 'http'
            domain = sites.Site.objects.get_current().domain
            base_url = '%s://%s' % (protocol, domain)
            view, args, kwargs = func(cart, uuid, order_form)
            return base_url + reverse(view, args=args, kwargs=kwargs)

