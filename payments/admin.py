from django.contrib import admin
from .models import DuesPayment

# Register your models here.
class DuesPaymentAdmin(admin.ModelAdmin):
	pass

admin.site.register(DuesPayment, DuesPaymentAdmin)