from django.conf.urls import url
from django.contrib import admin
from . import views


urlpatterns = [
    url(r'^add', views.new_member, name="new_member"),
    url(r'^thanks', views.member_thanks, name="member_thanks"),
]
