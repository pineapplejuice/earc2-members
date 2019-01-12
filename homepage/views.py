from urllib.parse import urlencode

from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone

from .models import Meeting, MeetingPlace, Event

# Create your views here.

GOOGLE_MAPS_API_KEY = 'AIzaSyB5U5s-pijWcGEi9TPqNk1AZyBr0BCcOZY'


def home_page(request):
	"""Render home page."""
	return render(request, 'homepage/home.html')
	
def about(request):
	"""Render about static page."""
	return render(request, 'homepage/about.html')

def meetings(request):
	"""Render meeting page with dates of upcoming meetings and 
	map of meeting place.
	"""	
	
	future_meetings = Meeting.objects.filter(
		date_time__gt=timezone.now()).order_by('date_time')
	next_meeting = future_meetings[0] if future_meetings.count() > 0 else None
	upcoming_meetings = future_meetings[1:] if future_meetings.count() < 4 else future_meetings[1:4]
	
	if next_meeting:
		meeting_place = next_meeting.meeting_place
		print(meeting_place)
		query = {
			'key': GOOGLE_MAPS_API_KEY,
			'q': '{}, {}, {} {}'.format(meeting_place.address, meeting_place.city, 
				meeting_place.state, meeting_place.zip_code),
		}

		map_url = "https://www.google.com/maps/embed/v1/place?" + urlencode(query)
		print(map_url)
	else:
		map_url = None

	context = {
		'next_meeting': next_meeting,
		'upcoming_meetings': upcoming_meetings,
		'next_meeting_map_url': map_url
	}
	
	return render(request, 'homepage/meetings.html', context)

def events(request):
	"""Render upcoming event list."""
	future_events = Event.objects.filter(start_date_time__gt=timezone.now())
	
	context = {
		'future_events': future_events,
	}
	
	return render(request, 'homepage/events.html', context)


def nets(request):
	"""Render net list."""
	return render(request, 'homepage/nets.html')
	
