from django.shortcuts import render
from django.http import HttpResponse

from .models import Meeting, MeetingPlace

# Create your views here.

def home_page(request):
	return render(request, 'homepage/home.html')
	
def about(request):
	return render(request, 'homepage/about.html')

def meetings(request):
	next_meeting = Meeting.objects.order_by('date_time')[0]
	upcoming_meetings = Meeting.objects.order_by('date_time')[1:3]

	context = {
		'next_meeting': next_meeting,
		'upcoming_meetings': upcoming_meetings,
	}
	
	return render(request, 'homepage/meetings.html', context)


