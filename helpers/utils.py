from django.core.mail import EmailMessage
from django.template.loader import render_to_string

class EmailMessageFromTemplate(EmailMessage):
    
    def __init__(self, subject_template, message_template, context, recipients, cc=None, reply_to=None):
        EmailMessage.__init__(
            self,
            subject=render_to_string(subject_template, context),
            body=render_to_string(message_template, context),
            to=recipients,
            cc=cc,
            reply_to=reply_to,
        )


def send_email_from_template(subject_template, message_template, context, recipients, cc = None, reply_to=None):
	"""
	Helper function to send email from template.
	subject_template (text, template filename)
	message_template (text, template filename)
	context (dictionary for template)
	recipients (list)
	cc (list)
	reply_to (list)
	"""
	
	# Render message
	subject = render_to_string(subject_template, context)
	message = render_to_string(message_template, context)
	email = EmailMessage(subject, message, to=recipients, cc=cc, reply_to=reply_to)
	email.send()
	
	return True

