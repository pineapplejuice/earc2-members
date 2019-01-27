import json
import requests

from datetime import date, datetime
from urllib.parse import urlencode

from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.urls import reverse

from helpers.utils import send_email_from_template

from .forms import MemberForm, UserForm
from .models import Member
from .tokens import account_activation_token


# Helper function
def redirect_params(url, params=None):
	"""Redirect to a given url or alias with query string parameters."""
	response = redirect(url)
	if params:
		query_string = urlencode(params)
		response['Location'] += '?' + query_string
	return response


# Views
def member_list(request):
	"""Render member list in pages."""
	members = Member.objects.order_by('callsign')
	paginator = Paginator(members, 20)	# 20 members per page
	
	page = request.GET.get('page')
	members=paginator.get_page(page)
	return render(request, "manage_members/member_list.html", 
		{'members': members})	

@login_required
def redirect_to_profile(request):
	"""Redirect to user's profile"""
	messages.success(request, 'You have successfully logged in.')
	return redirect("member_profile", request.user.member.id)

@login_required
def member_profile(request, id):
	"""Render member profile for logged in member."""
	member = get_object_or_404(Member, pk=id)
	if request.user.pk != member.user.pk:
		return render(request, "manage_members/member_permission_denied.html")
	
	return render(request, "manage_members/member_profile.html", 
		{'member': member})

	
@login_required
def member_update(request, id):
	"""Allow member to update information in database."""
	member = get_object_or_404(Member, pk=id)
	if request.user.pk != member.user.pk:
		return render(request, "manage_members/member_permission_denied.html")
	
	member_form = MemberForm(request.POST or None, instance = member)
	if member_form.is_valid():
		member_form.save()
		messages.success(request, 'Profile details updated.')
		return redirect('member_profile', id=id)
	return render(request, "manage_members/member_update_form.html", 
		{'member': member, 'member_form': member_form})


def new_member(request):
	"""Allow new member to setup user information and account password."""
	if request.method == 'POST':
		member_form = MemberForm(request.POST)
		user_form = UserForm(request.POST)
		if member_form.is_valid() and user_form.is_valid():

			# Save both forms without commiting yet
			member = member_form.save(commit=False)
			user = user_form.save(commit=False)
			
			uls_url = "http://data.fcc.gov/api/license-view/basicSearch/getLicenses?format=json&searchValue="
			try:
				res = requests.get(uls_url + member.callsign)
				res_unicode = res.content.decode('utf-8')
				res_json = json.loads(res_unicode)
				member.expiration_date = datetime.strptime(res_json['Licenses']['License'][0]['expiredDate'], '%m/%d/%Y').date()
			except ConnectionError:
				pass

			
			# Create the name, email, and username fields from the member information
			user.username = member.callsign.lower()
			user.email = member.email_address
			user.first_name = member.first_name
			user.last_name = member.last_name
			user.set_password(user.password)	# sets the password in hash
			user.is_active = False		# user needs to activate first
			user.save()					# save the user

			# Link user to member record and save member record
			member.user = User.objects.get(username = user.username)
			member.save()				
			
			# send confirmation email
			current_site = get_current_site(request) 
			send_email_from_template(
				subject="Activate your EARC member website account",
				message_template = 'manage_members/acc_active_email.txt',
				context = {
					'user': user,
					'member': member,
					'domain': current_site.domain,
					'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
					'token': account_activation_token.make_token(user),
				},
				recipients = [member.email_address],
			)			
			
			params = {
				'name': member_form.cleaned_data['first_name'],
			}
			
			return redirect_params('member_thanks', params)
	else:
		member_form = MemberForm(initial = {
			'expiration_date': date.today(), 
			'state': 'HI',
		})
		user_form = UserForm()
	
	return render(request, "manage_members/member_new_form.html", 
		{'member_form': member_form, 'user_form': user_form})


def member_thanks(request):
	"""Render message after submitting new member info."""
	context = {
		'name': request.GET.get('name'),
	}
	return render(request, "manage_members/member_thanks.html", context)


def activate(request, uidb64, token):
	"""Activate member based on URL given on activation email."""
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
