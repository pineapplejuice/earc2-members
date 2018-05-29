from django.conf.urls import url
from django.contrib import admin
from . import views


urlpatterns = [
    url(r'^add', views.new_member, name="member_form"),
    url(r'^thanks', views.member_thanks, name="member_thanks"),
]
