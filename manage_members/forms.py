import re
from datetime import date
from django import forms
from .models import Member

class MemberForm(forms.ModelForm):
	class Meta:
		model = Member
		fields = '__all__'
	
	def clean_callsign(self):
		data = self.cleaned_data['callsign'].upper()
		valid_call_regex = re.compile(r'^([A-Z0-9]{1,2})(\d)([A-Z]{1,3})$')
		if not valid_call_regex.match(data):
			raise forms.ValidationError('Not a valid callsign')
		return data

	def clean_expiration_date(self):
		data = self.cleaned_data['expiration_date']
		if data < date.today():
			raise forms.ValidationError('Your license has expired')
		return data
