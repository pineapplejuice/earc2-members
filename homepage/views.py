from urllib.parse import urlencode

from datetime import datetime, date, timedelta
from datetime import timezone as dt_timezone
from calendar import monthrange

from django.db.models import Q
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.urls import reverse
from django.utils import timezone
from paypal.standard.forms import PayPalPaymentsForm
from payments.paypal_helpers import paypal_email_test_or_prod

from helpers.utils import send_email_from_template
from homepage.forms import ContactForm
from homepage.models import Announcement, MeetingPlace, Event, LinkGroup, QuestionGroup
from manage_members.models import Member


# Create your views here.

GOOGLE_MAPS_API_KEY = 'AIzaSyB5U5s-pijWcGEi9TPqNk1AZyBr0BCcOZY'
HST = dt_timezone(-timedelta(hours=10))


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
    
    # future_meetings: pulls all meetings today or after
    future_meetings = Event.objects.filter(
        start_date_time__gte=timezone.now()).filter(
        event_category='MEETING').order_by('start_date_time')
    
    # next meeting is the first future meeting
    next_meeting = future_meetings[0] if future_meetings.count() > 0 else None
    
    # pull up to 3 more upcoming meetings
    upcoming_meetings = (future_meetings[1:] if future_meetings.count() < 4 
        else future_meetings[1:4])
    
    
    if next_meeting and next_meeting.event_venue.address:
        meeting_place = next_meeting.event_venue
        query = {
            'key': GOOGLE_MAPS_API_KEY,
            'q': '{}, {}, {} {}'.format(meeting_place.address, 
                meeting_place.city, meeting_place.state, 
                meeting_place.zip_code),
        }

        map_url = ("https://www.google.com/maps/embed/v1/place?" 
            + urlencode(query))
        print(map_url)
    else:
        map_url = None

    context = {
        'next_meeting': next_meeting,
        'upcoming_meetings': upcoming_meetings,
        'next_meeting_map_url': map_url
    }
    
    return render(request, 'homepage/meetings.html', context)


### Deprecated in favor of event calendar ###
def events(request):
    """
    Render upcoming event list.
    """
    
    future_events = Event.objects.filter(start_date_time__gt=timezone.now())
    
    context = {
        'future_events': future_events,
    }
    
    return render(request, 'homepage/events.html', context)


def view_event(request, id):
    
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
    return render(request, 'homepage/field_day.html')
    
def repeaters(request):
    return render(request, 'homepage/repeaters.html')

def antennas(request):
    
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
    
    form = PayPalPaymentsForm(initial = paypal_dict)
    context = {
        "form": form,
    }
    
    return render(request, 'homepage/antennas.html', context)

def antenna_purchase_completed(request):
    messages.success(
        request, 
        ("Thanks for your purchase. Our treasurer and antenna committee have "
         "received your order and will ship your antenna as soon as possible.")
    )
    return redirect("antennas")

def antenna_purchase_cancelled(request):
    messages.error(request, 'Your purchase was cancelled.')
    return redirect("antennas")
    
def swap_and_shop(request):
    return render(request, 'homepage/swap_shop.html')
    
def faq_list(request):
    groups = QuestionGroup.objects.all()
    context = {
        'groups': groups,
    }
    
    return render(request, 'homepage/faq.html', context)

def nh6wi(request):
    return render(request, 'homepage/nh6wi.html')
    
def contact(request):
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
                send_email_from_template(
                    subject_template = 'homepage/email/contact_form_subject.txt',
                    message_template = 'homepage/email/contact_form_body.txt',
                    context = context,
                    recipients = [webmaster_email],
                    reply_to = [contact_email],
                )
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('contact_success')
            
    return render(request, "homepage/contact.html", {'form': form})

def contact_success(request):
    return render(request, "homepage/contact_success.html")
    
def allmon(request):
    return render(request, "homepage/allmon.html")
    
def brandmeister(request):
    return render(request, "homepage/brandmeister.html")

def repeater_rules(request):
    return render(request, "homepage/repeater_rules.html")
    

## Event Calendar Code

##### Here's code for the view to look up the event objects for to put in 
# the context for the template. It goes in your app's views.py file (or 
# wherever you put your views).
#####

def named_month(month_number):
    """
    Return the name of the month, given the number.
    """
    return date(1900, month_number, 1).strftime("%B")

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
    my_calendar_to_month = datetime(my_year, my_month, monthrange(my_year, my_month)[1], tzinfo=HST)

    my_events = Event.objects.filter(start_date_time__gte=my_calendar_from_month).filter(start_date_time__lte=my_calendar_to_month)

    # Calculate values for the calendar controls. 1-indexed (Jan = 1)
    my_previous_year = my_year
    my_previous_month = my_month - 1
    if my_previous_month == 0:
        my_previous_year = my_year - 1
        my_previous_month = 12
    my_next_year = my_year
    my_next_month = my_month + 1
    if my_next_month == 13:
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

