from datetime import date
from urllib.parse import urlencode
from django.shortcuts import render, redirect
from .models import User
from .forms import MemberForm, UserForm

# Helper function
def redirect_params(url, params=None):
	"""Redirects to a given url or alias with query string parameters."""
	response = redirect(url)
	if params:
		query_string = urlencode(params)
		response['Location'] += '?' + query_string
	return response

# Email




# Views
def new_member(request):
	if request.method == 'POST':
		member_form = MemberForm(request.POST)
		user_form = UserForm(request.POST)
		if member_form.is_valid() and user_form.is_valid():

			member = member_form.save(commit=False)
			user = user_form.save(commit=False)
			
			user.username = member.callsign.lower()
			user.email = member.email_address
			user.first_name = member.first_name
			user.last_name = member.last_name
			user.set_password(user.password)
			user.is_active = False
			user.save()

			member.user = User.objects.get(username = user.username)
			member.save()
			
			
			
			
			params = {
				'name': member_form.cleaned_data['first_name'],
				'type': member_form.cleaned_data['app_type'],
			}
			
			return redirect_params('member_thanks', params)
	else:
		member_form = MemberForm(initial = {'expiration_date': date.today(), 'state': 'HI'})
		user_form = UserForm()
	
	return render(request, "manage_members/member_form.html", {'member_form': member_form, 'user_form': user_form})


def member_thanks(request):
	context = {
		'name': request.GET.get('name'),
		'type': request.GET.get('type'),
	}
	return render(request, "manage_members/member_thanks.html", context)
