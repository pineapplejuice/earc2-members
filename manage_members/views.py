from datetime import date
from urllib.parse import urlencode
from django.shortcuts import render, redirect

from .forms import MemberForm

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
		form = MemberForm(request.POST)
		if form.is_valid():
			params = {
				'name': form.cleaned_data['first_name'],
				'type': form.cleaned_data['app_type'],
			}
			
			
			
			form.save()
			return redirect_params('member_thanks', params)
	else:
		form = MemberForm(initial = {'expiration_date': date.today(), 'state': 'HI'})
	
	return render(request, "manage_members/member_form.html", {'form': form})


def member_thanks(request):
	context = {
		'name': request.GET.get('name'),
		'type': request.GET.get('type'),
	}
	return render(request, "manage_members/member_thanks.html", context)
