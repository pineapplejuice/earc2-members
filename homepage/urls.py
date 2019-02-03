from django.conf.urls import url
from . import views


urlpatterns = [
	url(r'^about/$', views.about, name="about"),
	url(r'^antennas/$', views.antennas, name="antennas"),
	url(r'^antennas/success/$', views.antenna_purchase_completed, 
		name="antenna_purchase_completed"),
	url(r'^antennas/cancelled/$', views.antenna_purchase_cancelled,
		name="antenna_purchase_cancelled"),
	url(r'^events/$', views.events, name="events"),
	url(r'^faq-list/$', views.faq_list, name="faq_list"),
	url(r'^field_day/$', views.field_day, name="field_day"),
	url(r'^links/$', views.links, name="links"),
	url(r'^meetings/$', views.meetings, name="meetings"),
	url(r'^nets/$', views.nets, name="nets"),
	url(r'^officers/$', views.officers, name="officers"),
	url(r'^repeaters/$', views.repeaters, name="repeaters"),
	url(r'^swap-shop/$', views.swap_and_shop, name="swap_and_shop"),
]