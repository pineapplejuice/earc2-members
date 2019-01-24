from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
	url(r'^dues/(?P<id>[0-9]+)/$', views.pay_dues_paypal, name="pay_dues_paypal"),
]
