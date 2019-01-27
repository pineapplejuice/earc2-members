from django.core.exceptions import ValidationError

from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received

from .paypal_helpers import paypal_email_test_or_prod

from payments.models import DuesPayment
from manage_members.models import Member

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

		# Check if item and price is valid
		if ipn_obj.item_number not in ['RENEW', 'NEWQ1', 'NEWQ2', 'NEWQ3', 'NEWQ4']:
			return
		else:
			item_num = ipn_obj.item_number
			if item_num == "RENEW":
				price = 20.0
			elif item_num[0:3] == "NEW":
				price = 5.0 * (5 - int(item_num[-1]))
		
		if ipn_obj.mc_gross == price and ipn_obj.mc_currency == 'USD':
			
			parse_custom = ipn_obj.custom.split('-')
			print(parse_custom)
			
			member_id = int(parse_custom[0])
			membership_year = int(parse_custom[1])
			
			new_payment = DuesPayment(
				payment_date = ipn_obj.payment_date,
				membership_year = membership_year,
				member = Member.objects.get(pk=member_id),
				dues_type = ipn_obj.item_number,
				payment_method = 'PP',
				ref_number = ipn_obj.txn_id,
				amount = ipn_obj.mc_gross,
			)
			new_payment.save()
			
	else:
		return

valid_ipn_received.connect(show_me_the_money)