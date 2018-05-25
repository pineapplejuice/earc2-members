from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import MemberForm

# Create your views here.
def new_member(request):
	if request.method == 'POST':
		form = MemberForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/member/thanks')
	else:
		form = MemberForm()			
	
	return render(request, "member_form.html", {'form': form})

def member_thanks(request):
	return render(request, "member_thanks.html")