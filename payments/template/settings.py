# # Dotted package path and class name of the function that
# # is called on submit of the payment checkout step. This is where
# # integration with a payment gateway should be implemented.
# SHOP_HANDLER_PAYMENT = # path.to.primary.processor


###################
# PAYMENT OPTIONS #
###################

SECONDARY_PAYMENT_PROCESSORS = (
    ('payment-key', { 'name' : 'Friendly Name', 'form' : 'dot.separarted.form.Class' }),
    ('payment-key', { 'name' : 'Friendly Name', 'form' : 'dot.separarted.form.Class' })
)
