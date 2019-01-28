from django.core.mail import EmailMessage
from django.template.loader import render_to_string

def send_email_from_template(subject_template, message_template, context, recipients, cc = None):
	"""
	Helper function to send email from template.
	subject_template (text, template filename)
	message_template (text, template filename)
	context (dictionary for template)
	recipients (list)
	"""
	
	# Render message
	subject = render_to_string(subject_template, context)
	message = render_to_string(message_template, context)
	email = EmailMessage(subject, message, to=recipients, cc=cc)
	email.send()
	
	return True

