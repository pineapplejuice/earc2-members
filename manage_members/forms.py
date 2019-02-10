import re
from datetime import date
from django.forms import (
	ModelForm, RadioSelect, SelectDateWidget, 
	PasswordInput, HiddenInput, CharField, ValidationError
)
from django.contrib.auth.models import User
from .models import Member

## Constants ##

# Looks for (1 or 2 alphanumeric)(one digit)(up to three letters)
CALLSIGN_VALIDATOR = r'^([A-Z0-9]{1,2})(\d)([A-Z]{1,3})$'

# Default list of choices for Yes or No
YES_NO_DROPDOWN = [(True, 'Yes'), (False, 'No')]

## Models ##

class MemberForm(ModelForm):
	class Meta:
		model = Member
		exclude = ['position',]
		widgets = {
			'expiration_date': HiddenInput(),
			'mailing_list': RadioSelect(choices=YES_NO_DROPDOWN),
			'wd_online': RadioSelect(choices=YES_NO_DROPDOWN),
			'arrl_member': RadioSelect(choices=YES_NO_DROPDOWN),
			'need_new_badge': RadioSelect(choices=YES_NO_DROPDOWN),
			'user': HiddenInput(),
		}
	
	
	def clean_callsign(self):
		data = self.cleaned_data['callsign'].upper()
		valid_call_regex = re.compile(CALLSIGN_VALIDATOR)
		if not valid_call_regex.match(data):
			raise ValidationError('Not a valid callsign')
		return data

	def clean_expiration_date(self):
		data = self.cleaned_data['expiration_date']
		if data < date.today():
			raise ValidationError('Your license has expired')
		return data


class UserForm(ModelForm):
	password = CharField(widget=PasswordInput())
	confirm_password = CharField(widget=PasswordInput())
	
	class Meta:
		model = User
		fields = ('password',)
	
	def clean(self):
		cleaned_data = super(UserForm, self).clean()
		password = cleaned_data.get('password')
		confirm_password = cleaned_data.get('confirm_password')
		
		if password != confirm_password:
			raise ValidationError("Password and confirm password do not match")

