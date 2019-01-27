from django.contrib import admin
from .models import DuesPayment

# Register your models here.
class DuesPaymentAdmin(admin.ModelAdmin):
	list_display = ('payment_date', 'membership_year', 'member', 'dues_type', 'payment_method', 'amount')

admin.site.register(DuesPayment, DuesPaymentAdmin)
