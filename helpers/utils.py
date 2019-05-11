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


