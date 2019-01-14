from django.conf.urls import url
from . import views


urlpatterns = [
	url(r'^about/$', views.about, name="about"),
	url(r'^meetings/$', views.meetings, name="meetings"),
	url(r'^officers/$', views.officers, name="officers"),
	url(r'^nets/$', views.nets, name="nets"),
	url(r'^events/$', views.events, name="events"),
]