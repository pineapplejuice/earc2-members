import re
from datetime import date
from django.forms import (
	ModelForm, RadioSelect, SelectDateWidget, 
	PasswordInput, HiddenInput, CharField, ValidationError,
	NumberInput, EmailInput,
)
from django.contrib.auth.models import User
from .models import Member

## Constants ##

# Looks for (1 or 2 alphanumeric)(one digit)(up to three letters)
CALLSIGN_VALIDATOR = r'^([A-Z0-9]{1,2})(\d)([A-Z]{1,3})$'

# Default list of choices for Yes or No
YES_NO_DROPDOWN = [(True, 'Yes'), (False, 'No')]

## Helpers ##
def capitalize_address(input):
	words = input.split()
	output_words = []
	for word in words:
		if word.lower() == 'po' or word.lower() == 'p.o.':
			output_words.append('PO')
		else:
			output_words.append(word.capitalize())
	return ' '.join(output_words)

def numbers_only_phone(input):
	output = []
	for char in list(input):
		if char.isdigit():
			output.append(char)
	return ''.join(output)

## Models ##

class MemberForm(ModelForm):
	class Meta:
		model = Member
		exclude = ['position',]
		widgets = {
			'expiration_date': HiddenInput(),
			'email_address': EmailInput(),
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

	def clean_first_name(self):
		return self.cleaned_data['first_name'].capitalize()
	
	def clean_last_name(self):
		return self.cleaned_data['last_name'].capitalize()
	
	def clean_address(self):
		return capitalize_address(self.cleaned_data['address'])
	
	def clean_city(self):
		return capitalize_address(self.cleaned_data['city'])
	
	def clean_phone(self):
		data = numbers_only_phone(self.cleaned_data['phone'])
		if len(data) != 10:
			if len(data) == 7:
				data = '808' + data
			else:
				raise ValidationError('Invalid phone number')
		return data

	def clean_email_address(self):
		return self.cleaned_data['email_address'].lower()

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

