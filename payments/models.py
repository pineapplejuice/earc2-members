import datetime

from django.db import models
from django.db.models import signals, Max
from django.utils.timezone import now

from manage_members.models import Member

# Create your models here.

# Dropdown lists
from helpers.models import DUES_TYPE

PAYMENT_METHOD = [
	('CASH', 'Cash'),
	('CHK', 'Check'),
	('PP', 'PayPal'),
]


# Model
class DuesPayment(models.Model):
	payment_date = models.DateField()
	membership_year = models.IntegerField()
	member = models.ForeignKey(Member, on_delete=models.CASCADE)
	dues_type = models.CharField(max_length=5, choices=DUES_TYPE)
	payment_method = models.CharField(max_length=4, choices=PAYMENT_METHOD)
	ref_number = models.CharField(max_length=50, blank=True)
	amount = models.DecimalField(max_digits=5, decimal_places=2)

