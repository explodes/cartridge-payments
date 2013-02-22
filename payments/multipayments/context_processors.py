from mezzanine.conf import settings


def required_context(request):

    return {
        'PRIMARY_PAYMENT_PROCESSOR_IN_USE' : settings.PRIMARY_PAYMENT_PROCESSOR_IN_USE
    }
