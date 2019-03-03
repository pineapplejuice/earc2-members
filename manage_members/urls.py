from django.conf.urls import url
from django.contrib import admin

from manage_members import views


urlpatterns = [
	url(r'^(?P<id>[0-9]+)/$', views.member_profile, name="member_profile"),
	url(r'^(?P<id>[0-9]+)/update/$', views.member_update, 
	    name="member_update"),
    url(r'^add/$', views.new_member, name="member_new_form"),
    url(r'^list/$', views.member_list, name="member_list"),
    url(r'^thanks/$', views.member_thanks, name="member_thanks"),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-'
        '[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
]
