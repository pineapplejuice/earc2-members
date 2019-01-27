from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received

from .paypal_helpers import paypal_email_test_or_prod

def show_me_the_money(sender, **kwargs):
    ipn_obj = sender
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        # WARNING !
        # Check that the receiver email is the same we previously
        # set on the `business` field. (The user could tamper with
        # that fields on the payment form before it goes to PayPal)
        if ipn_obj.receiver_email != paypal_email_test_or_prod():
            # Not a valid payment
            return

        # ALSO: for the same reason, you need to check the amount
        # received, `custom` etc. are all what you expect or what
        # is allowed.

        # Undertake some action depending upon `ipn_obj`.
        if ipn_obj.custom == "premium_plan":
            price = ...
        else:
            price = ...

        if ipn_obj.mc_gross == price and ipn_obj.mc_currency == 'USD':
            ...
    else:
        return

valid_ipn_received.connect(show_me_the_money)