import datetime
import pytz

from django.conf import settings
from django.contrib.auth.models import User
from django.core import mail
from django.core.exceptions import ValidationError
from django.test import TestCase, override_settings
from django.utils import timezone
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from manage_members.models import Member
from manage_members.forms import MemberForm, UserForm
from manage_members.tokens import account_activation_token

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
            password='Pa$$word1',
        ),
    )
    return member

def setup_member_2():
    member = Member.objects.create(
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
    return member

def setup_member_1_dict():
    data = {
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
    return data


class TestMemberViews(TestCase):
    def setUp(self):
        self.test_member1 = setup_member_1()
        self.test_member2 = setup_member_2()

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

    def test_view_other_member_profile_with_no_user_while_logged_in(self):
        self.test_member2.user = None
        self.client.force_login(user=self.test_member1.user)
        response = self.client.get(f'/member/{self.test_member2.pk}/')
        self.assertTemplateUsed(response, 'manage_members/member_permission_denied.html')

    def test_view_nonexistent_profile_while_logged_in(self):
        self.client.force_login(user=self.test_member1.user)
        response = self.client.get(f'/member/3/')
        self.assertEquals(response.status_code, 404)


class TestNewMemberForm(TestCase):
    def setUp(self):
        self.test_data = setup_member_1_dict()
    
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

    @override_settings(
        GOOGLE_RECAPTCHA_SITE_KEY='6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI')
    @override_settings(
        GOOGLE_RECAPTCHA_SECRET_KEY='6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe')
    def test_new_member_form_fails_with_missing_member_data(self):
        self.test_data['last_name'] = ''
        response = self.client.post('/member/add/', self.test_data)
        self.assertTemplateUsed(response, 'manage_members/member_new_form.html')
        self.assertIsNotNone(response.context['member_form'].errors)

    @override_settings(
        GOOGLE_RECAPTCHA_SITE_KEY='6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI')
    @override_settings(
        GOOGLE_RECAPTCHA_SECRET_KEY='6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe')
    def test_new_member_form_fails_with_invalid_member_data(self):
        self.test_data['email_address'] = 'invalidemail'
        response = self.client.post('/member/add/', self.test_data)
        self.assertTemplateUsed(response, 'manage_members/member_new_form.html')
        self.assertIsNotNone(response.context['member_form'].errors)

    @override_settings(
        GOOGLE_RECAPTCHA_SITE_KEY='6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI')
    @override_settings(
        GOOGLE_RECAPTCHA_SECRET_KEY='6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe')
    def test_new_member_form_fails_with_invalid_user_data(self):
        self.test_data['confirm_password'] = ''
        response = self.client.post('/member/add/', self.test_data)
        self.assertTemplateUsed(response, 'manage_members/member_new_form.html')
        self.assertIsNotNone(response.context['user_form'].errors)


class TestUserActivation(TestCase):
    def setUp(self):
        self.test_member = setup_member_1()

        self.test_user = User.objects.get(username='kh6tst')
        self.test_user.is_active = False
        self.test_user.save()
        self.uidb64 = urlsafe_base64_encode(
            force_bytes(self.test_user.pk)).decode()
        self.token = account_activation_token.make_token(self.test_user)
        self.test_url = ('/member/activate/' + self.uidb64 + '/' 
                         + self.token + '/')

    def test_setup_user_starts_off_inactive(self):
        self.assertFalse(User.objects.get(username='kh6tst').is_active)

    def test_successful_user_activation(self):
        response = self.client.get(self.test_url)
        self.assertRedirects(response, '/member/activate/success/')
        self.assertTrue(User.objects.get(username='kh6tst').is_active)

    def test_invalid_activation_token_fails(self):
        self.token = 'invalidinvalidinvalid'
        self.test_url = ('/member/activate/' + self.uidb64 + '/' 
                         + self.token + '/')
        response = self.client.get(self.test_url)
        self.assertRedirects(response, '/member/activate/failed/')
        self.assertFalse(User.objects.get(username='kh6tst').is_active)
    
    def test_activation_token_invalid_after_login(self):
        response = self.client.get(self.test_url)
        self.assertRedirects(response, '/member/activate/success/')
        self.assertTrue(User.objects.get(username='kh6tst').is_active)
        
        self.client.login(user='kh6tst', password='Pa$$word1')
        self.client.logout()
        
        response = self.client.get(self.test_url)
        self.assertRedirects(response, '/member/activate/failed/')
        self.assertTrue(User.objects.get(username='kh6tst').is_active)


class TestMemberUpdateForm(TestCase):
    def setUp(self):
        self.test_member1 = setup_member_1()
        self.test_member2 = setup_member_2()

    def test_test_case_setup(self):
        self.assertEquals(Member.objects.count(), 2)
        self.assertEquals(User.objects.count(), 2)

    def test_anonymous_user_must_login_to_access_update_form(self):
        response = self.client.get(f'/member/{self.test_member1.pk}/update/')
        self.assertRedirects(
            response, 
            f'/accounts/login/?next=/member/{self.test_member1.pk}/update/')

    def test_logged_in_user_can_access_update_form(self):
        self.client.force_login(user=self.test_member1.user)
        response = self.client.get(f'/member/{self.test_member1.pk}/update/')
        self.assertTemplateUsed(response, 
                                'manage_members/member_update_form.html')
        self.assertIsInstance(response.context['member_form'], MemberForm)
        self.assertEquals(response.context['member_form'].instance, 
                          self.test_member1)
    
    def test_logged_in_user_cannot_access_update_form_for_someone_else(self):
        self.client.force_login(user=self.test_member1.user)
        response = self.client.get(f'/member/{self.test_member2.pk}/update/')
        self.assertTemplateUsed(
            response, 
            'manage_members/member_permission_denied.html')

    def test_logged_in_member1_cannot_access_member2_with_no_user(self):
        self.client.force_login(user=self.test_member1.user)
        self.test_member2.user = None
        response = self.client.get(f'/member/{self.test_member2.pk}/update/')
        self.assertTemplateUsed(
            response, 
            'manage_members/member_permission_denied.html')

    def test_successfully_updates_with_valid_data(self):
        self.client.force_login(user=self.test_member1.user)
        url = f'/member/{self.test_member1.pk}/update/'
        response = self.client.get(url)
        data = response.context['member_form'].initial
        data['address'] = "789 Mahalo St"
        response = self.client.post(url, data)
        
        # redirects to member profile
        self.assertRedirects(response, f'/member/{self.test_member1.pk}/')
        
        # emails sent
        self.assertEquals(len(mail.outbox), 1)
        self.assertEquals(mail.outbox[0].subject, 
                          "Member account updated: John Operator, KH6TST")
        self.assertIn("789 Mahalo St", mail.outbox[0].body)
        
        # record updated
        member = Member.objects.get(pk=self.test_member1.pk)
        self.assertEquals(member.address, "789 Mahalo St")
    
    def test_update_with_missing_data_fails(self):
        self.client.force_login(user=self.test_member1.user)
        url = f'/member/{self.test_member1.pk}/update/'
        response = self.client.get(url)
        data = response.context['member_form'].initial
        data['address'] = ''
        response = self.client.post(url, data)
        
        self.assertTemplateUsed(response, 'manage_members/member_update_form.html')
        self.assertIsNotNone(response.context['member_form'].errors)
    
    def test_update_with_invalid_data_fails(self):
        self.client.force_login(user=self.test_member1.user)
        url = f'/member/{self.test_member1.pk}/update/'
        response = self.client.get(url)
        data = response.context['member_form'].initial
        data['email_address'] = 'invalidemailaddress'
        response = self.client.post(url, data)
        
        self.assertTemplateUsed(response, 'manage_members/member_update_form.html')
        self.assertIsNotNone(response.context['member_form'].errors)
