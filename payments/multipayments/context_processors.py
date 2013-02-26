from mezzanine.conf import settings as conf


def settings(request):
    ppp_in_use = conf.PRIMARY_PAYMENT_PROCESSOR_IN_USE
    return {
        'PRIMARY_PAYMENT_PROCESSOR_IN_USE' : ppp_in_use
    }
