from django.core.mail import EmailMessage
from django.template.loader import render_to_string

def send_email_from_template(subject, message_template, context, recipients):
	"""
	Helper function to send email from template.
	subject (text)
	message_template (text, template filename)
	context (dictionary for template)
	recipients (list)
	"""
	
	# Render message
	message = render_to_string(message_template, context)
	email = EmailMessage(subject, message, to=recipients)
	email.send()
	
	return True

