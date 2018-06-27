from django.db import models
from django.db.models import signals, Max
from django.utils.timezone import now
from django.contrib.auth.models import User
import datetime

# Create your models here.

# Dropdown lists

DUES_TYPE = [
	('N', 'New member'),
	('R', 'Renewal'),
]

PAYMENT_METHOD = [
	('CASH', 'Cash'),
	('CHK', 'Check'),
	('PP', 'PayPal'),
]

LICENSE_TYPES = [
	('T', 'Technician'),
	('G', 'General'),
	('A', 'Advanced'),
	('E', 'Extra'),
]


# Helper functions
def update_user(sender, instance, created, **kwargs):
	"""Updates username and user demographics when member model changes"""
	if not created:
		user = instance.user
		user.username = instance.callsign.lower()
		user.email = instance.email_address
		user.first_name = instance.first_name
		user.last_name = instance.last_name
		user.save()


class Member(models.Model):
	callsign = models.CharField(max_length=6)
	license_type = models.CharField(max_length=1, choices=LICENSE_TYPES)
	expiration_date = models.DateField(
		verbose_name = "My license expires",
	)
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	address = models.CharField(max_length=95)
	city = models.CharField(max_length=35)
	state = models.CharField(max_length=2)
	zip_code = models.CharField(max_length=10)
	phone = models.CharField(max_length=10)
	email_address = models.EmailField()
	mailing_list = models.BooleanField(
		verbose_name = "Add me to the club mailing list"
	)
	wd_online = models.BooleanField(
		verbose_name = "I would like to read the Wireless Dispatch online"
	)
	arrl_member = models.BooleanField(
		verbose_name = "I am an ARRL member"
	)
	need_new_badge = models.BooleanField(
		verbose_name = "I need a new membership badge"
	)
	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
	
	
	def __str__(self):
		return self.first_name + ' ' + self.last_name + ', ' + self.callsign
	
	def get_absolute_url(self):
		from django.urls import reverse
		return reverse('member_profile', args=[str(self.id)])
		
	def last_dues_payment(self):
		d = self.duespayment_set.aggregate(latest_payment=Max('payment_date'))
		return d['latest_payment']
	
	def membership_expires(self):
		d = self.duespayment_set.aggregate(latest_year=Max('membership_year'))
		return datetime.date(d['latest_year'], 12, 31)
	
	def membership_status(self):
		_today = datetime.date.today()
		
		if self.duespayment_set.count() == 0:
			return "P"
		elif self.membership_expires() > _today:
			return "C"
		elif membership_expires().year > _today.year - 3:
			return "LR"
		else:
			return "LN"


signals.post_save.connect(update_user, sender=Member)


class DuesPayment(models.Model):
	payment_date = models.DateField()
	membership_year = models.IntegerField()
	member = models.ForeignKey(Member, on_delete=models.CASCADE)
	dues_type = models.CharField(max_length=1, choices=DUES_TYPE)
	payment_method = models.CharField(max_length=4, choices=PAYMENT_METHOD)
	ref_number = models.CharField(max_length=50, blank=True)
	amount = models.DecimalField(max_digits=5, decimal_places=2)
	