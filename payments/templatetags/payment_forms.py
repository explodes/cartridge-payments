from mezzanine import template
from mezzanine.conf import settings

register = template.Library()

@register.as_tag
def payment_forms(request, order_form):
    processors = settings.SECONDARY_PAYMENT_PROCESSORS
    forms = []
    for dummy_key, processor in processors.iteritems():
        name = processor['name']
        form_class_name = processor['form']
        form_class = get_callable(form_class_name)
        form = form_class(request, order_form)
        forms.append((name, form))
    return forms
