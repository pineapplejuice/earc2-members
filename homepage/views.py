from django.shortcuts import render


# Create your views here.

def home_page(request):
	return render(request, 'homepage/home.html')
	
def about(request):
	return render(request, 'homepage/about.html')
	
