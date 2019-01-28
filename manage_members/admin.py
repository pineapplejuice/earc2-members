from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Member

# Register your models here.

class MemberAdmin(admin.ModelAdmin):
	def full_name(self, obj):
		return f"{obj.first_name} {obj.last_name}"
	full_name.short_description = "Full name"
	
	list_display = ('callsign', 'full_name', 'position')

class UserAdmin(BaseUserAdmin):
    pass
    

	
admin.site.register(Member, MemberAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)