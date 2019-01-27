import json
import requests
from requests.exceptions import ConnectionError
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
		
def get_ngrok_url():
	url = "http://localhost:4040/api/tunnels"
	try:
		res = requests.get(url)
	except ConnectionError as e:
		print("Warning: ngrok not activated. PayPal IPN will not function correctly.")
		return "http://localhost:8000"
	res_unicode = res.content.decode("utf-8")
	res_json = json.loads(res_unicode)
	return res_json["tunnels"][1]["public_url"]

	
