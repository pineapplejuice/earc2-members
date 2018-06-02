from django.db import models

# Create your models here.
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
	
	def __str__(self):
		return str(self.date_time) + ', ' + self.meeting_place.venue_name


