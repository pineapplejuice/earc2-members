from earc2.settings import PAYPAL_TEST

def paypal_email_test_or_prod():
	"""
	Returns the appropriate account depending on whether PayPal is set for sandbox 
	(PAYPAL_TEST = True) or production (PAYPAL_TEST = False).
	"""
	if PAYPAL_TEST:
		return 'treasurer-facilitator@earchi.org'
	else:
		return 'treasurer@earchi.org'