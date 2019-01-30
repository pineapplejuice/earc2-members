from django.contrib import admin
from .models import Announcement, Meeting, MeetingPlace, Event, LinkGroup, Link

# Register your models here.

class AnnouncementAdmin(admin.ModelAdmin):
	def title(obj):
		return obj.title
	
	def text(obj):
		return obj.text
		
	def date_created(obj):
		return obj.date_created
	
	list_display = ('title', 'text', 'date_created')

class MeetingPlaceAdmin(admin.ModelAdmin):
	list_display = ('venue_name', 'address', 'city', 'state', 'zip_code')
	
class MeetingAdmin(admin.ModelAdmin):
	list_display = ('date_time', 'meeting_place', 'topic')

class EventAdmin(admin.ModelAdmin):
	pass

class LinkGroupAdmin(admin.ModelAdmin):
	list_display = ('name',)

class LinkAdmin(admin.ModelAdmin):
	list_display = ('name', 'url', 'description', 'group')
	

admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(MeetingPlace, MeetingPlaceAdmin)
admin.site.register(Meeting, MeetingAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(LinkGroup, LinkGroupAdmin)
admin.site.register(Link, LinkAdmin)


