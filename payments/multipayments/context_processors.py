from mezzanine.conf import settings


def required_context(request):
    ppp_in_use = settings.PRIMARY_PAYMENT_PROCESSOR_IN_USE
    return {
        'PRIMARY_PAYMENT_PROCESSOR_IN_USE' : ppp_in_use
    }
