from django.contrib import admin
from .models import Meeting, MeetingPlace
# Register your models here.

class MeetingPlaceAdmin(admin.ModelAdmin):
	pass
	
class MeetingAdmin(admin.ModelAdmin):
	pass

admin.site.register(MeetingPlace, MeetingPlaceAdmin)
admin.site.register(Meeting, MeetingAdmin)
