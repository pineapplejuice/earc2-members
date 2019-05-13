from django.urls import path, re_path
from django.contrib import admin

from manage_members import views


urlpatterns = [
    path('<int:id>/', views.member_profile, name="member_profile"),
    path('<int:id>/update/', views.member_update, name="member_update"),
    path('add/', views.new_member, name="member_new_form"),
    path('list/', views.member_list, name="member_list"),
    path('thanks/', views.member_thanks, name="member_thanks"),
    path('activate/<str:uidb64>/<str:token>/', views.activate, name='activate'),
    path('activate/success/', 
         views.activation_successful, name="activation_successful"),
    path('activate/failed/', 
         views.activation_failed, name="activation_failed"),
]
