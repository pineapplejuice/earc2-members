import datetime
import pytz

from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.utils import timezone
from django.core import mail
from django.core.exceptions import ValidationError
from manage_members.models import Member
from manage_members.forms import MemberForm, UserForm

home_tz = pytz.timezone("Pacific/Honolulu")

class TestMemberViews(TestCase):
    def setUp(self):
        self.test_member1 = Member.objects.create(
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
                password='Pa$$word1',
            ),
        )

        self.test_member2 = Member.objects.create(
            callsign='KH6XXX',
            license_type='E',
            expiration_date=home_tz.localize(datetime.datetime(2019,9,22)),
            first_name='Mary',
            last_name='Operator',
            address='123 Aloha St',
            city='Honolulu',
            state='HI',
            zip_code='96813',
            phone='8085551212',
            email_address='test1@test1.com',
            mailing_list=True,
            wd_online=True,
            arrl_member=True,
            need_new_badge=True,
            user=User.objects.create_user(
                username='kh6xxx',
                email='test1@test1.com',
                first_name='Mary',
                last_name='Operator',
                password='Pa$$word2',
            ),
        )

    def test_view_member_profile_while_logged_in(self):
        self.client.force_login(user=self.test_member1.user)
        response = self.client.get(f'/member/{self.test_member1.pk}/')
        self.assertTemplateUsed(response, 'manage_members/member_profile.html')

    def test_view_member_profile_while_not_logged_in(self):
        response = self.client.get(f'/member/{self.test_member1.pk}/')
        self.assertRedirects(response, f'/accounts/login/?next=/member/{self.test_member1.pk}/')
    
    def test_view_other_member_profile_while_logged_in(self):
        self.client.force_login(user=self.test_member1.user)
        response = self.client.get(f'/member/{self.test_member2.pk}/')
        self.assertTemplateUsed(response, 'manage_members/member_permission_denied.html')
     
    def test_view_nonexistent_profile_while_logged_in(self):
        self.client.force_login(user=self.test_member1.user)
        response = self.client.get(f'/member/3/')
        self.assertEquals(response.status_code, 404)


class TestNewMemberForm(TestCase):
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
            'password': 'Pa$$word1',
            'confirm_password': 'Pa$$word1',
        }
    
    def test_new_member_form_initially_renders_unbound(self):
        response = self.client.get('/member/add/')
        self.assertTemplateUsed(response, 'manage_members/member_new_form.html')
        self.assertIsInstance(response.context['member_form'], MemberForm)
        self.assertFalse(response.context['member_form'].is_bound)
        self.assertIsInstance(response.context['user_form'], UserForm)
        self.assertFalse(response.context['user_form'].is_bound)

    @override_settings(
        GOOGLE_RECAPTCHA_SITE_KEY='6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI')
    @override_settings(
        GOOGLE_RECAPTCHA_SECRET_KEY='6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe')
    def test_new_member_form_posts_successfully_valid_data(self):
        response = self.client.post('/member/add/', self.test_data)
        
        # Member and user should be created
        self.assertEquals(Member.objects.count(), 1)
        self.assertEquals(User.objects.count(), 1)
        
        # Member and user should refer to each other
        member_found = Member.objects.get(
            callsign=self.test_data['callsign'])
        self.assertEquals(member_found.callsign, self.test_data['callsign'])
        user_found = member_found.user
        self.assertEquals(user_found.username, 
                          self.test_data['callsign'].lower())
                          
        # User information is correct
        self.assertTrue(user_found.check_password(
                        self.test_data['password']))
        self.assertFalse(user_found.is_active)
        
        # Emails sent
        self.assertEquals(len(mail.outbox), 2)
        
        self.assertEquals(mail.outbox[0].subject, 
                          "Activate your EARC member account")
        self.assertIn(self.test_data['email_address'], 
                      mail.outbox[0].to)
        
        self.assertEquals(mail.outbox[1].subject,
                          "Member account created: John Operator, KH6TST")
        self.assertEquals(settings.MEMBERSHIP_ADMINS, mail.outbox[1].to)

    def test_new_member_form_fails_with_missing_member_data(self):
        self.test_data['last_name'] = ''
        response = self.client.post('/member/add/', self.test_data)
        self.assertTemplateUsed(response, 'manage_members/member_new_form.html')
        self.assertIsNotNone(response.context['member_form'].errors)

    def test_new_member_form_fails_with_invalid_member_data(self):
        self.test_data['email_address'] = 'invalidemail'
        response = self.client.post('/member/add/', self.test_data)
        self.assertTemplateUsed(response, 'manage_members/member_new_form.html')
        self.assertIsNotNone(response.context['member_form'].errors)

    def test_new_member_form_fails_with_invalid_user_data(self):
        self.test_data['confirm_password'] = ''
        response = self.client.post('/member/add/', self.test_data)
        self.assertTemplateUsed(response, 'manage_members/member_new_form.html')
        self.assertIsNotNone(response.context['user_form'].errors)

