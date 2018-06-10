from django.contrib import admin
from .models import Meeting, MeetingPlace, Event
# Register your models here.

class MeetingPlaceAdmin(admin.ModelAdmin):
	pass
	
class MeetingAdmin(admin.ModelAdmin):
	pass

class EventAdmin(admin.ModelAdmin):
	pass

admin.site.register(MeetingPlace, MeetingPlaceAdmin)
admin.site.register(Meeting, MeetingAdmin)
admin.site.register(Event, EventAdmin)

