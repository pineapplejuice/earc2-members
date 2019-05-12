import datetime
import pytz

from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError
from manage_members.models import Member
from manage_members.forms import MemberForm, UserForm

home_tz = pytz.timezone("Pacific/Honolulu")

class TestMemberFormValidation(TestCase):
    def setUp(self):
        self.test_data = {
            'callsign': 'KH6TST',
            'license_type': 'E',
            'first_name': 'John',
            'last_name': 'Operator',
            'address': '1234 Aloha Way',
            'city': 'Honolulu',
            'state': 'HI',
            'zip_code': '96813',
            'phone': '8085551212',
            'email_address': 'test@test.com',
            'mailing_list': True,
            'wd_online': True,
            'arrl_member': True,
            'need_new_badge': True,
        }
    
    def test_validate_baseline_case_valid(self):
        form = MemberForm(self.test_data)
        self.assertEquals(form.is_valid(), True)
    
    def test_validate_missing_callsign_fails(self):
        # Prospective members with no license should contact membership to 
        # be added to member roll manually via admin panel.
        self.test_data['callsign'] = ''
        form = MemberForm(self.test_data)
        self.assertEquals(form.is_valid(), False)
    
    def test_validate_invalid_callsign_fails(self):
        self.test_data['callsign'] = 'NOCALL'
        form = MemberForm(self.test_data)
        self.assertEquals(form.is_valid(), False)

    def test_validate_missing_license_type_fails(self):
        # Prospective members with no license should contact membership to 
        # be added to member roll manually via admin panel.
        self.test_data['license_type'] = ''
        form = MemberForm(self.test_data)
        self.assertEquals(form.is_valid(), False)
    
    def test_validate_invalid_license_type_fails(self):
        self.test_data['license_type'] = 'X'
        form = MemberForm(self.test_data)
        self.assertEquals(form.is_valid(), False)
    
    def test_validate_missing_first_name_fails(self):
        self.test_data['first_name'] = ''
        form = MemberForm(self.test_data)
        self.assertEquals(form.is_valid(), False)

    def test_validate_missing_last_name_fails(self):
        self.test_data['last_name'] = ''
        form = MemberForm(self.test_data)
        self.assertEquals(form.is_valid(), False)

    def test_validate_missing_address_fails(self):
        self.test_data['address'] = ''
        form = MemberForm(self.test_data)
        self.assertEquals(form.is_valid(), False)
    
    def test_validate_missing_city_fails(self):
        self.test_data['city'] = ''
        form = MemberForm(self.test_data)
        self.assertEquals(form.is_valid(), False)

    def test_validate_missing_state_fails(self):
        self.test_data['state'] = ''
        form = MemberForm(self.test_data)
        self.assertEquals(form.is_valid(), False)
    
    def test_validate_missing_zip_code_fails(self):
        self.test_data['zip_code'] = ''
        form = MemberForm(self.test_data)
        self.assertEquals(form.is_valid(), False)
    
    def test_validate_invalid_zip_code_fails(self):
        self.test_data['zip_code'] = 'V3R 2E0'
        form = MemberForm(self.test_data)
        self.assertEquals(form.is_valid(), False)
    
    def test_validate_missing_phone_number_fails(self):
        self.test_data['phone'] = ''
        form = MemberForm(self.test_data)
        self.assertEquals(form.is_valid(), False)

    def test_validate_missing_email_address_fails(self):
        self.test_data['email_address'] = ''
        form = MemberForm(self.test_data)
        self.assertEquals(form.is_valid(), False)

    def test_validate_invalid_email_address_fails(self):
        self.test_data['email_address'] = 'invalidemailaddress'
        form = MemberForm(self.test_data)
        self.assertEquals(form.is_valid(), False)

class TestUserCreateFormValidation(TestCase):
    
    def setUp(self):
        self.test_data = {
            'password': 'MyPa$$w0rd',
            'confirm_password': 'MyPa$$w0rd',
        }
    
    def test_validate_baseline_case_valid(self):
        form = UserForm(self.test_data)
        self.assertEquals(form.is_valid(), True)
    
    def test_validate_missing_password_field_fails(self):
        self.test_data['password'] = ''
        form = UserForm(self.test_data)
        self.assertEquals(form.is_valid(), False)
    
    def test_validate_missing_confirm_password_field_fails(self):
        self.test_data['confirm_password'] = ''
        form = UserForm(self.test_data)
        self.assertEquals(form.is_valid(), False)
    
    def test_validate_password_and_confirm_password_mismatch_fails(self):
        self.test_data['confirm_password'] = 'Mi$matcH!99'
        form = UserForm(self.test_data)
        self.assertEquals(form.is_valid(), False)
