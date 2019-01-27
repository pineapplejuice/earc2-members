from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from paypal.standard.forms import PayPalPaymentsForm

from .paypal_helpers import paypal_email_test_or_prod, get_ngrok_url
from manage_members.models import Member


# Create your views here.

@login_required
def pay_dues_paypal(request, id):
	
	# Retrieve matching member and deny access if not member logged in
	member = get_object_or_404(Member, pk=id)
	if request.user.pk != member.user.pk:
		return render(request, "manage_members/member_permission_denied.html")
	
	# Pass member year and id to Paypal to track payment
	custom_string = str(member.pk) + "-" + str(member.member_dues_year())
	
	# What you want the button to do
	paypal_dict = {
		'business': paypal_email_test_or_prod(),
		'amount': f"{member.member_dues_amount():.2f}",
		'item_name': member.member_dues_description(),
		'item_number': member.member_dues_type(),
		'custom': custom_string,
		"notify_url": (
			request.build_absolute_uri(reverse('paypal-ipn')) if not settings.DEBUG
			else get_ngrok_url() + reverse('paypal-ipn')
		),
		"return": request.build_absolute_uri(reverse('paypal_completed')), 
		"cancel_return": request.build_absolute_uri(reverse('paypal_cancelled')),
	}
	
	
	form = PayPalPaymentsForm(initial = paypal_dict)
	context = {
		"member": member,
		"form": form,
	}

	return render(request, "payments/pay_dues_paypal.html", context)
	
@login_required
def paypal_cancelled(request):
		
	messages.error(request, "Your payment attempt was cancelled. Please try again.")
	return redirect("member_profile", request.user.member.id)


@login_required
def paypal_completed(request):
		
	messages.success(request, "Your PayPal payment was successful. It may take a few minutes for your membership status to be updated.")
	return redirect("member_profile", request.user.member.id)