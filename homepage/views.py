from django.shortcuts import render
from django.http import HttpResponse
from urllib.parse import urlencode


from .models import Meeting, MeetingPlace

# Create your views here.

GOOGLE_MAPS_API_KEY = 'AIzaSyB5U5s-pijWcGEi9TPqNk1AZyBr0BCcOZY'

def home_page(request):
	return render(request, 'homepage/home.html')
	
def about(request):
	return render(request, 'homepage/about.html')

def meetings(request):
	next_meeting = Meeting.objects.order_by('date_time')[0]
	upcoming_meetings = Meeting.objects.order_by('date_time')[1:3]
		
	meeting_place = next_meeting.meeting_place
	query = {
		'key': GOOGLE_MAPS_API_KEY,
		'q': '{}, {}, {} {}'.format(meeting_place.address, meeting_place.city, meeting_place.state, meeting_place.zip_code),
	}

	map_url = "https://www.google.com/maps/embed/v1/place?" + urlencode(query)
	print(map_url)

	context = {
		'next_meeting': next_meeting,
		'upcoming_meetings': upcoming_meetings,
		'next_meeting_map_url': map_url
	}
	
	return render(request, 'homepage/meetings.html', context)


