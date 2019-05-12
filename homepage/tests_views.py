import datetime
import pytz

from django.test import TestCase
from django.utils import timezone
from manage_members.models import Member

home_tz = pytz.timezone("Pacific/Honolulu")

# Create your tests here.
class TestRenderNonFormPages(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.president = Member.objects.create(
            callsign='AH6XX',
            license_type='E',
            expiration_date=home_tz.localize(datetime.datetime(2019,9,22)),
            first_name='Club',
            last_name='President',
            address='123 Aloha St',
            city='Honolulu',
            state='HI',
            zip_code='96813',
            phone='(808) 555-1212',
            email_address='president@earchi.org',
            mailing_list=True,
            wd_online=True,
            arrl_member=True,
            need_new_badge=True,
            position='PR',
        )

        cls.vice_president = Member.objects.create(
            callsign='AH6VP',
            license_type='E',
            expiration_date=home_tz.localize(datetime.datetime(2019,9,22)),
            first_name='Club',
            last_name='Vice-President',
            address='456 Aloha St',
            city='Honolulu',
            state='HI',
            zip_code='96813',
            phone='(808) 555-1313',
            email_address='vp@earchi.org',
            mailing_list=True,
            wd_online=True,
            arrl_member=True,
            need_new_badge=True,
            position='VP',
        )
        
        cls.secretary = Member.objects.create(
            callsign='AH6SE',
            license_type='E',
            expiration_date=home_tz.localize(datetime.datetime(2019,9,22)),
            first_name='Club',
            last_name='Secretary',
            address='789 Aloha St',
            city='Honolulu',
            state='HI',
            zip_code='96813',
            phone='(808) 555-1414',
            email_address='secretary@earchi.org',
            mailing_list=True,
            wd_online=True,
            arrl_member=True,
            need_new_badge=True,
            position='SE',
        )
        
        cls.treasurer = Member.objects.create(
            callsign='AH6TR',
            license_type='E',
            expiration_date=home_tz.localize(datetime.datetime(2019,9,22)),
            first_name='Club',
            last_name='Treasurer',
            address='789 Aloha St',
            city='Honolulu',
            state='HI',
            zip_code='96813',
            phone='(808) 555-1414',
            email_address='treasurer@earchi.org',
            mailing_list=True,
            wd_online=True,
            arrl_member=True,
            need_new_badge=True,
            position='TR',
        )
        
        cls.director = Member.objects.create(
            callsign='AH6DI',
            license_type='E',
            expiration_date=home_tz.localize(datetime.datetime(2019,9,22)),
            first_name='Club',
            last_name='Director',
            address='789 Aloha St',
            city='Honolulu',
            state='HI',
            zip_code='96813',
            phone='(808) 555-1414',
            email_address='director1@earchi.org',
            mailing_list=True,
            wd_online=True,
            arrl_member=True,
            need_new_badge=True,
            position='DI',
        )
        
    def _test_page(self, url, template):
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template)

    def test_render_home_page(self):
        self._test_page('/', template='homepage/home.html')
    
    def test_render_about_page(self):
        self._test_page('/homepage/about/', template='homepage/about.html')
    
    def test_render_antennas_page(self):
        self._test_page('/homepage/antennas/', 
                        template='homepage/antennas.html')

    def test_render_contact_page(self):
        self._test_page('/homepage/contact/', template='homepage/contact.html')
    
    def test_render_events_calendar(self):
        self._test_page('/homepage/events/', 
                        template='homepage/event_calendar.html')
    
    def test_render_particular_month_calendar(self):
        self._test_page('/homepage/events/calendar/2019/12/', 
                        template='homepage/event_calendar.html')
        
    def test_render_faq_page(self):
        self._test_page('/homepage/faq-list/', template='homepage/faq.html')
    
    def test_render_field_day_page(self):
        self._test_page('/homepage/field-day/', 
                        template='homepage/field_day.html')

    def test_render_links_page(self):
        self._test_page('/homepage/links/', template='homepage/links.html')
    
    def test_render_meetings_page(self):
        self._test_page('/homepage/meetings/', 
                        template='homepage/meetings.html')
    
    def test_render_nets_page(self):
        self._test_page('/homepage/nets/', template='homepage/nets.html')
    
    def test_render_nh6wi_weather_page(self):
        self._test_page('/homepage/nh6wi/', template='homepage/nh6wi.html')
    
    def test_render_officers_page(self):
        self._test_page('/homepage/officers/', 
                        template='homepage/officers.html')

    def test_render_repeaters_page(self):
        self._test_page('/homepage/repeaters/', template='homepage/repeaters.html')
    
    def test_render_brandmeister_page(self):
        self._test_page('/homepage/repeaters/brandmeister/', 
                        template='homepage/brandmeister.html')
    
    def test_render_repeater_logbook_page(self):
        self._test_page('/homepage/repeaters/logbook/', 
                        template='homepage/logbook.html')

    def test_render_repeater_rules_page(self):
        self._test_page('/homepage/repeaters/rules/', 
                        template='homepage/repeater_rules.html')
    
    def test_render_swap_and_shop_page(self):
        self._test_page('/homepage/swap-shop/', 
                        template='homepage/swap_shop.html')
