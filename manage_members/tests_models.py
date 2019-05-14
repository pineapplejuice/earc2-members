import datetime
import pytz

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError
from manage_members.models import Member

home_tz = pytz.timezone("Pacific/Honolulu")

def setup_member_1():
    member = Member.objects.create(
        callsign='KH6TST',
        license_type='E',
        expiration_date=home_tz.localize(datetime.datetime(2019,9,22)),
        first_name='John',
        last_name='Operator',
        address='123 Aloha St',
        city='Honolulu',
        state='HI',
        zip_code='96813',
        phone='8085551212',
        email_address='test@test.com',
        mailing_list=True,
        wd_online=True,
        arrl_member=True,
        need_new_badge=True,
        user=User.objects.create_user(
            username='kh6tst',
            email='test@test.com',
            first_name='John',
            last_name='Operator',
        ),
    )
    member.user.set_password('Pa$$word1')
    member.user.save()
    return member


class TestMemberModelValidation(TestCase):
    def setUp(self):
        self.test_member = setup_member_1()

    def test_baseline_dataset_valid(self):
        self.test_member.full_clean()
    
    def test_validate_missing_callsign_OK(self):
        self.test_member.callsign = ''
        self.test_member.full_clean()

    def test_validate_invalid_callsign_fails(self):
        self.test_member.callsign = 'NOCALL'
        with self.assertRaises(ValidationError):
            self.test_member.full_clean()
    
    def test_validate_missing_license_type_OK(self):
        self.test_member.license_type = ''
        self.test_member.full_clean()
    
    def test_validate_invalid_license_type_fails(self):
        self.test_member.license_type = 'X'
        with self.assertRaises(ValidationError):
            self.test_member.full_clean()
    
    def test_validate_missing_expiration_date_OK(self):
        self.test_member.expiration_date = None
        self.test_member.full_clean()

    def test_validate_missing_first_name_fails(self):
        self.test_member.first_name = ''
        with self.assertRaises(ValidationError):
            self.test_member.full_clean()

    def test_validate_missing_last_name_fails(self):
        self.test_member.last_name = ''
        with self.assertRaises(ValidationError):
            self.test_member.full_clean()
    
    def test_validate_missing_address_fails(self):
        self.test_member.address = ''
        with self.assertRaises(ValidationError):
            self.test_member.full_clean()
    
    def test_validate_missing_city_fails(self):
        self.test_member.city = ''
        with self.assertRaises(ValidationError):
            self.test_member.full_clean()
    
    def test_validate_missing_state_fails(self):
        self.test_member.state = ''
        with self.assertRaises(ValidationError):
            self.test_member.full_clean()
    
    def test_validate_missing_zip_code_fails(self):
        self.test_member.zip_code = ''
        with self.assertRaises(ValidationError):
            self.test_member.full_clean()

    def test_validate_invalid_zip_code_fails(self):
        self.test_member.zip_code = 'V3R 2E0'
        with self.assertRaises(ValidationError):
            self.test_member.full_clean()
    
    def test_validate_missing_phone_fails(self):
        self.test_member.phone = ''
        with self.assertRaises(ValidationError):
            self.test_member.full_clean()
    
    def test_validate_missing_email_address_fails(self):
        self.test_member.email_address = ''
        with self.assertRaises(ValidationError):
            self.test_member.full_clean()

    def test_validate_invalid_email_address_fails(self):
        self.test_member.email_address = 'invalidemailaddress'
        with self.assertRaises(ValidationError):
            self.test_member.full_clean()

    def test_validate_missing_mailing_list_flag_fails(self):
        self.test_member.mailing_list = None
        with self.assertRaises(ValidationError):
            self.test_member.full_clean()
    
    def test_validate_missing_online_newsletter_flag_fails(self):
        self.test_member.wd_online = None
        with self.assertRaises(ValidationError):
            self.test_member.full_clean()
    
    def test_validate_missing_arrl_member_flag_fails(self):
        self.test_member.arrl_member = None
        with self.assertRaises(ValidationError):
            self.test_member.full_clean()
    
    def test_validate_missing_member_badge_flag_fails(self):
        self.test_member.need_new_badge = None
        with self.assertRaises(ValidationError):
            self.test_member.full_clean()


class TestMemberUserInteraction(TestCase):
    def setUp(self):
        self.test_member = setup_member_1()
    
    def test_callsign_update_updates_associated_username(self):
        self.test_member.callsign = "KH6NEW"
        self.test_member.save()
        self.assertEquals(
            User.objects.get(pk=self.test_member.user.pk).username, 
            'kh6new')
    
    def test_name_update_updates_associated_user(self):
        self.test_member.first_name = 'Jim'
        self.test_member.save()
        self.assertEquals(
            User.objects.get(pk=self.test_member.user.pk).first_name,
            'Jim')

    def test_email_update_updates_associated_user(self):
        self.test_member.email_address = 'newemail@test.com'
        self.test_member.save()
        self.assertEquals(
            User.objects.get(pk=self.test_member.user.pk).email,
            'newemail@test.com')
