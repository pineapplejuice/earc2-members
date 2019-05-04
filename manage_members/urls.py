from django.urls import path, re_path
from django.contrib import admin

from manage_members import views


urlpatterns = [
    path('<int:id>/', views.member_profile, name="member_profile"),
    path('<int:id>/update/', views.member_update, name="member_update"),
    path('add/', views.new_member, name="member_new_form"),
    path('list/', views.member_list, name="member_list"),
    path('thanks/', views.member_thanks, name="member_thanks"),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-'
        '[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
]
