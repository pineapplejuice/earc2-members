import datetime
import pytz

from django.test import TestCase
from django.utils import timezone
from homepage.forms import ContactForm

class TestContactForm(TestCase):
    def setUp(self):
        self.test_data = {
            'contact_name': 'Test User',
            'contact_email': 'test@test.com',
            'contact_message': 'This is a test message.'
        }
    
    def test_validate_baseline_data_valid(self):
        form = ContactForm(self.test_data)
        self.assertEquals(form.is_valid(), True)
    
    def test_validate_missing_name_fails(self):
        self.test_data['contact_name'] = ''
        form = ContactForm(self.test_data)
        self.assertEquals(form.is_valid(), False)
    
    def test_validate_missing_email_fails(self):
        self.test_data['contact_email'] = ''
        form = ContactForm(self.test_data)
        self.assertEquals(form.is_valid(), False)
    
    def test_validate_invalid_email_fails(self):
        self.test_data['contact_email'] = 'invalidemailaddress'
        form = ContactForm(self.test_data)
        self.assertEquals(form.is_valid(), False)
    
    def test_validate_missing_message_text_fails(self):
        self.test_data['contact_message'] = ''
        form = ContactForm(self.test_data)
        self.assertEquals(form.is_valid(), False)
