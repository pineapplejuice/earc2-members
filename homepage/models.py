from datetime import timedelta
from time import strftime

from django.db import models
from django.urls import reverse
from django.utils import timezone

# Constant lists

EVENT_CATEGORIES = [
    ('MEETING', 'Meeting'),
    ('TESTING', 'Testing Session'),
    ('SOCIAL', 'Social Event'),
    ('OTHER', 'Other Event'),
]


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


class Event(models.Model):
    event_category = models.CharField(
        max_length=10,
        choices=EVENT_CATEGORIES,
        blank=True)
    start_date_time = models.DateTimeField()
    end_date_time = models.DateTimeField()
    event_name = models.CharField(max_length=100)
    event_venue = models.ForeignKey(MeetingPlace, on_delete=models.CASCADE)
    description = models.TextField(blank=True)

    def get_event_date(self):
        return timezone.localtime(self.start_date_time).strftime('%B %d, %Y, %I:%M %p')
        
    def get_event_time(self):
        return timezone.localtime(self.start_date_time).time().strftime('%I:%M %p')

    def __str__(self):
        return str(self.get_event_date()) + ', ' + self.event_name
    
    def get_absolute_url(self):
        return reverse('view_event', args=[str(self.id)])
    

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


class QuestionGroup(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return str(self.name)


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    answer_text = models.TextField()
    group = models.ForeignKey(QuestionGroup, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.question_text)



