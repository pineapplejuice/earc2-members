from earc2.settings import PAYPAL_TEST

def paypal_email_test_or_prod():
	if PAYPAL_TEST:
		return 'treasurer-facilitator@earchi.org'
	else:
		return 'treasurer@earchi.org'