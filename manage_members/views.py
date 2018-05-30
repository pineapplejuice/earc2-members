from datetime import date
from urllib.parse import urlencode

from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


from .forms import MemberForm, UserForm
from .models import Member
from django.contrib.auth.models import User
from .tokens import account_activation_token


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
			
			# send confirmation email
			current_site = get_current_site(request)
			mail_subject = "Activate your EARC member website account"
			
			message = render_to_string('manage_members/acc_active_email.html', {
				'user': user,
				'member': member,
				'domain': current_site.domain,
				'uid': urlsafe_base64_encode(force_bytes(user.pk)),
				'token': account_activation_token.make_token(user),
			})
			to_email = member.email_address
			email = EmailMessage(mail_subject, message, to=[to_email])
			email.send()
			
			
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


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        print("User found")
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
        print("User not found")
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # return redirect('home')
        return render(request, "manage_members/member_activation_success.html")
    else:
        return render(request, "manage_members/member_activation_failed.html")
