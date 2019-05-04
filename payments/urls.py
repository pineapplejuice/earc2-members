from django.urls import path, re_path
from django.contrib import admin
from . import views

urlpatterns = [
    path('dues/<int:id>/', views.pay_dues_paypal, name="pay_dues_paypal"),
    path('cancelled/', views.paypal_cancelled, name="paypal_cancelled"),
    path('completed/', views.paypal_completed, name="paypal_completed"),
]
