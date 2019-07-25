from django.test import TestCase
from django.core import mail

from helpers.utils import EmailMessageFromTemplate

class TestEmailTemplate(TestCase):
    def setUp(self):
        self.test_email = EmailMessageFromTemplate(
            subject_template='manage_members/email/contact_form_subject.txt',
            message_template='manage_members/email/contact_form_body.txt',
            context={
                'contact_name': 'Test User',
                'contact_email': 'test@test.com',
                'contact_message': 'This is a test message.',
            },
            recipients=['webmaster@earchi.org'],
        )
    
    def test_email_send(self):
        self.test_email.send()
        
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Message received from test@test.com')
        self.assertEqual(mail.outbox[0].to, ['webmaster@earchi.org'])
        self.assertRegex(mail.outbox[0].body, "This is a test message")
