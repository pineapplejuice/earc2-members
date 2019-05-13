from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from paypal.standard.forms import PayPalPaymentsForm

from payments.paypal_helpers import paypal_email_test_or_prod, get_ngrok_url
from manage_members.models import Member
from manage_members.views import logged_in_user_matches_requested_user



def _get_notify_url(request):
    """
    If in dev mode, set to ngrok URL listener so that it redirects to this 
    machine.  Else, set to domain paypal IPN listener.
    """
    if not settings.DEBUG:
        return request.build_absolute_url(reverse('paypal-ipn'))
    else:
        return get_ngrok_url() + reverse('paypal-ipn')


def _initialize_paypal_button(request, member):
    """
    Set up PayPal button, including email address, item, and 
    other PayPal parameters.
    """
    # Pass member year and id to Paypal to track payment
    custom_string = str(member.pk) + "-" + str(member.member_dues_year())
    
    # What you want the button to do
    paypal_dict = {
        'business': paypal_email_test_or_prod(),
        'amount': f"{member.member_dues_amount():.2f}",
        'item_name': member.member_dues_description(),
        'item_number': member.member_dues_type(),
        'custom': custom_string,
        "notify_url": _get_notify_url(request),
        "return": request.build_absolute_uri(reverse('paypal_completed')), 
        "cancel_return": request.build_absolute_uri(
            reverse('paypal_cancelled')),
    }
    
    return PayPalPaymentsForm(initial = paypal_dict)


@login_required
def pay_dues_paypal(request, id):
    """
    Render dues payment page.
    """
    treasurer = Member.objects.get(position='TR')
    
    # Retrieve matching member and deny access if not member logged in
    member = get_object_or_404(Member, pk=id)
    if not logged_in_user_matches_requested_user(request, member):
        return render(request, "manage_members/member_permission_denied.html")

    context = {
        "member": member,
        "form": _initialize_paypal_button(request, member),
        "treasurer": treasurer,
    }

    return render(request, "payments/pay_dues_paypal.html", context)
    
@login_required
def paypal_cancelled(request):
        
    messages.error(
        request, "Your payment attempt was cancelled. Please try again.")
    return redirect("member_profile", request.user.member.id)


@login_required
def paypal_completed(request):
        
    messages.success(
        request, 
        ("Your PayPal payment was successful. "
         "It may take a few minutes for your membership status to be updated.")
    )
    return redirect("member_profile", request.user.member.id)