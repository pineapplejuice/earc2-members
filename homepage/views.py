"""
homepage/views.py
"""

from urllib.parse import urlencode

from datetime import datetime, date, timedelta
from datetime import timezone as dt_timezone
from calendar import monthrange

from django.db.models import Q
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import (
    render, redirect, get_object_or_404, render_to_response)
from django.http import HttpResponse
from django.template import RequestContext
from django.urls import reverse
from django.utils import timezone
from paypal.standard.forms import PayPalPaymentsForm
from payments.paypal_helpers import paypal_email_test_or_prod
import pytz

from helpers.utils import EmailMessageFromTemplate
from homepage.forms import ContactForm
from homepage.models import (
    Announcement, MeetingPlace, Event, LinkGroup,
    LogbookEntry, QuestionGroup,
)
from manage_members.models import Member


# Create your views here.

GOOGLE_MAPS_API_KEY = 'AIzaSyB5U5s-pijWcGEi9TPqNk1AZyBr0BCcOZY'
HST = dt_timezone(-timedelta(hours=10))

timezone.activate(pytz.timezone("Pacific/Honolulu"))


def home_page(request):
    """Render home page."""

    announcements = Announcement.objects.filter(
        Q(expiration_date__isnull=True) |
        Q(expiration_date__gte=timezone.now())
    ).order_by('-date_created')

    context = {
        'announcements': announcements,
    }

    return render(request, 'homepage/home.html', context)


def about(request):
    """Render about static page."""
    return render(request, 'homepage/about.html')


def officers(request):
    """Render officers page (pulls members with specific titles)."""

    president = Member.objects.get(position='PR')
    vice_pres = Member.objects.get(position='VP')
    secretary = Member.objects.get(position='SE')
    treasurer = Member.objects.get(position='TR')
    directors = Member.objects.filter(position='DI')

    context = {
        'president': president,
        'vice_pres': vice_pres,
        'secretary': secretary,
        'treasurer': treasurer,
        'directors': directors,
    }

    return render(request, 'homepage/officers.html', context)


def meetings(request):
    """
    Render meeting page with dates of next four upcoming meetings and
    map of meeting place.
    """
    next_meeting, upcoming_meetings = get_future_meetings()

    context = {
        'next_meeting': next_meeting,
        'upcoming_meetings': upcoming_meetings,
        'next_meeting_map_url': get_google_maps_url(next_meeting)
                                if next_meeting else None
    }

    return render(request, 'homepage/meetings.html', context)

def get_future_meetings():
    future_meetings = Event.objects.filter(
        start_date_time__gte=timezone.now()).filter(
            event_category='MEETING').order_by('start_date_time')

    next_meeting = future_meetings[0] if future_meetings.count() > 0 else None
    
    upcoming_meetings = (future_meetings[1:] if future_meetings.count() < 4
                         else future_meetings[1:4])

    return next_meeting, upcoming_meetings

def get_google_maps_url(next_meeting):
    if next_meeting.event_venue.address:
        meeting_place = next_meeting.event_venue
        query = {
            'key': GOOGLE_MAPS_API_KEY,
            'q': '{}, {}, {} {}'.format(meeting_place.address,
                                        meeting_place.city,
                                        meeting_place.state,
                                        meeting_place.zip_code),
        }

        map_url = ("https://www.google.com/maps/embed/v1/place?"
                   + urlencode(query))
    else:
        map_url = None

    return map_url


def view_event(request, id):
    """
    View single event by primary key.
    """
    
    context = {
        'event': get_object_or_404(Event, pk=id),
    }

    return render(request, 'homepage/view_event.html', context)


def nets(request):
    """
    Render net list.
    """

    return render(request, 'homepage/nets.html')


def links(request):
    """
    Render links list.
    """

    groups = LinkGroup.objects.all()
    context = {
        'groups': groups,
    }

    return render(request, 'homepage/links.html', context)

def field_day(request):
    """
    Render field day page.
    """
    return render(request, 'homepage/field_day.html')

def repeaters(request):
    """
    Render repeater information page.
    """
    return render(request, 'homepage/repeaters.html')

def antennas(request):
    """
    Initialize paypal information and render antenna information page. 
    Page includes link to PayPal.
    """
    paypal_dict = {
        'business': paypal_email_test_or_prod(),
        'amount': "56.00",
        'item_name': "6 to 40 Meter End Fed",
        'item_number': "ENDFED",
        "return": request.build_absolute_uri(
            reverse('antenna_purchase_completed')),
        "cancel_return": request.build_absolute_uri(
            reverse('antenna_purchase_cancelled')),
    }

    context = {
        "form": PayPalPaymentsForm(initial=paypal_dict),
    }

    return render(request, 'homepage/antennas.html', context)

def antenna_purchase_completed(request):
    """
    Render antenna purchase confirmation page.
    """
    messages.success(
        request,
        ("Thanks for your purchase. Our treasurer and antenna committee have "
         "received your order and will ship your antenna as soon as possible.")
    )
    return redirect("antennas")

def antenna_purchase_cancelled(request):
    """
    Render antenna purchase cancel page.
    """
    
    messages.error(request, 'Your purchase was cancelled.')
    return redirect("antennas")

def swap_and_shop(request):
    """
    Render swap and shop page.
    """
    return render(request, 'homepage/swap_shop.html')

def faq_list(request):
    """
    Render membership FAQ list.
    """
    context = {
        'groups': QuestionGroup.objects.all(),
    }

    return render(request, 'homepage/faq.html', context)

def nh6wi(request):
    """
    Render page for Edward NH6WI.
    """
    return render(request, 'homepage/nh6wi.html')

def contact(request):
    """
    Render contact form.
    """
    webmaster_email = 'keith.higa@gmail.com'

    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_name = form.cleaned_data['contact_name']
            contact_email = form.cleaned_data['contact_email']
            contact_message = form.cleaned_data['contact_message']

            try:
                context = {
                    'contact_name': contact_name,
                    'contact_email': contact_email,
                    'contact_message': contact_message,
                }
                EmailMessageFromTemplate(
                    subject_template='homepage/email/contact_form_subject.txt',
                    message_template='homepage/email/contact_form_body.txt',
                    context=context,
                    recipients=[webmaster_email],
                    reply_to=[contact_email],
                ).send()

            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('contact_success')

    return render(request, "homepage/contact.html", {'form': form})

def contact_success(request):
    """
    Render contact success form.
    """
    return render(request, "homepage/contact_success.html")

def allmon(request):
    """
    Render allmon page.
    """
    return render(request, "homepage/allmon.html")

def brandmeister(request):
    """
    Render brandmeister information page.
    """
    return render(request, "homepage/brandmeister.html")

def repeater_rules(request):
    """
    Render repeater rules.
    """
    return render(request, "homepage/repeater_rules.html")

def logbook(request):
    """
    Render repeater logbook.
    """
    logbook = LogbookEntry.objects.all()
    context = {
        'logbook': logbook,
    }
    return render(request, "homepage/logbook.html", context)


def this_month(request):
    """
    Show calendar of events this month.
    """
    today = datetime.now()
    return calendar(request, today.year, today.month)
    

def calendar(request, year, month):
    """
    Show calendar of events for a given month of a given year.
    """

    my_year = int(year)
    my_month = int(month)
    my_calendar_from_month = datetime(my_year, my_month, 1, tzinfo=HST)
    my_calendar_to_month = datetime(my_year, my_month,
                                    monthrange(my_year, my_month)[1],
                                    tzinfo=HST)

    my_events = Event.objects.filter(
        start_date_time__gte=my_calendar_from_month).filter(
            start_date_time__lte=my_calendar_to_month)

    # Calculate values for the calendar controls. 1-indexed (Jan = 1)
    BEFORE_YEAR_BEGINNING = 0
    AFTER_YEAR_END = 13
    
    my_previous_year = my_year
    my_previous_month = my_month - 1
    if my_previous_month == BEFORE_YEAR_BEGINNING:
        my_previous_year = my_year - 1
        my_previous_month = 12
    my_next_year = my_year
    my_next_month = my_month + 1
    if my_next_month == AFTER_YEAR_END:
        my_next_year = my_year + 1
        my_next_month = 1
    my_year_after_this = my_year + 1
    my_year_before_this = my_year - 1

    context = {'events_list': my_events,
               'month': my_month,
               'month_name': named_month(my_month),
               'year': my_year,
               'previous_month': my_previous_month,
               'previous_month_name': named_month(my_previous_month),
               'previous_year': my_previous_year,
               'next_month': my_next_month,
               'next_month_name': named_month(my_next_month),
               'next_year': my_next_year,
               'year_before_this': my_year_before_this,
               'year_after_this': my_year_after_this,
              }

    return render(request, "homepage/event_calendar.html", context)

def named_month(month_number):
    """
    Return the name of the month, given the number.
    """
    return date(1900, month_number, 1).strftime("%B")

