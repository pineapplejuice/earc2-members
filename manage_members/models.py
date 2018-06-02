from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

# Create your models here.

# Dropdown lists

APP_TYPES = [
	('N', 'New Member'),
	('R', 'Renewal'),
	('U', 'Update Info'),
]

LICENSE_TYPES = [
	('T', 'Technician'),
	('G', 'General'),
	('A', 'Advanced'),
	('E', 'Extra'),
]



class Member(models.Model):
	app_type = models.CharField(max_length=1, choices=APP_TYPES,
		verbose_name = "Application type"
	)
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
	


