from django.db import models
from datetime import timedelta

# Create your models here.

class Announcement(models.Model):
	date_created = models.DateTimeField(auto_now_add=True)
	title = models.CharField(max_length=50, blank=False)
	text = models.TextField(blank=False)
	
	def expiration_date(self):
		return self.date_created + timedelta(days=30)
	


class MeetingPlace(models.Model):
	venue_name = models.CharField(max_length = 50)
	address = models.CharField(max_length = 95)
	city = models.CharField(max_length=35)
	state = models.CharField(max_length=2)
	zip_code = models.CharField(max_length=10)

	def __str__(self):
		return self.venue_name

	

class Meeting(models.Model):
	date_time = models.DateTimeField()
	meeting_place = models.ForeignKey(MeetingPlace, on_delete=models.CASCADE)
	topic = models.CharField(max_length=200, blank=True)
	
	def __str__(self):
		return str(self.date_time) + ', ' + self.meeting_place.venue_name


class Event(models.Model):
	start_date_time = models.DateTimeField()
	end_date_time = models.DateTimeField()
	event_name = models.CharField(max_length=100)
	event_venue = models.ForeignKey(MeetingPlace, on_delete=models.CASCADE)
	description = models.TextField(blank=True)
	
	def __str__(self):
		return str(self.start_date_time) + ', ' + self.event_name

class LinkGroup(models.Model):
	name = models.CharField(max_length=100)
	
	def __str__(self):
		return str(self.name)

class Link(models.Model):
	name = models.CharField(max_length=100)
	url = models.URLField()
	description = models.TextField(blank=True)
	group = models.ForeignKey(LinkGroup, on_delete=models.CASCADE)

	def __str__(self):
		return str(self.name)
