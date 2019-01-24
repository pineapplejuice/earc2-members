from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from manage_members.models import Member

# Create your views here.

@login_required
def pay_dues_paypal(request, id):
	
	# Retrieve matching member and deny access if not member logged in
	member = get_object_or_404(Member, pk=id)
	if request.user.pk != member.user.pk:
		return render(request, "manage_members/member_permission_denied.html")
	return render(request, "payments/pay_dues_paypal.html", {"member": member})