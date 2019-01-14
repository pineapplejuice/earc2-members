import re
from datetime import date
from django.forms import (
	ModelForm, Select, SelectDateWidget, 
	PasswordInput, HiddenInput, CharField, ValidationError
)
from django.contrib.auth.models import User
from .models import Member

class MemberForm(ModelForm):
	class Meta:
		model = Member
		exclude = ['position',]
		widgets = {
			'expiration_date': SelectDateWidget(
					years=list(range(date.today().year - 10, date.today().year + 11)),
				),
			'mailing_list': Select(choices=[(True, 'Yes'), (False, 'No')]),
			'wd_online': Select(choices=[(True, 'Yes'), (False, 'No')]),
			'arrl_member': Select(choices=[(True, 'Yes'), (False, 'No')]),
			'need_new_badge': Select(choices=[(True, 'Yes'), (False, 'No')]),
			'user': HiddenInput(),
		}
	
	
	def clean_callsign(self):
		data = self.cleaned_data['callsign'].upper()
		valid_call_regex = re.compile(r'^([A-Z0-9]{1,2})(\d)([A-Z]{1,3})$')
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

