from django.conf.urls import url
from . import views


urlpatterns = [
	url(r'^about/$', views.about, name="about"),
	url(r'^antennas/$', views.antennas, name="antennas"),
	url(r'^events/$', views.events, name="events"),
	url(r'^field_day/$', views.field_day, name="field_day"),
	url(r'^links/$', views.links, name="links"),
	url(r'^meetings/$', views.meetings, name="meetings"),
	url(r'^nets/$', views.nets, name="nets"),
	url(r'^officers/$', views.officers, name="officers"),
	url(r'^repeaters/$', views.repeaters, name="repeaters"),
]