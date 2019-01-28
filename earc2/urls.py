"""earc2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.urls import path
from django.contrib import admin
from django.views.generic import TemplateView
from homepage import views as homepage_views
from manage_members import views as member_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', homepage_views.home_page, name="home_page"),
    url(r'^robots\.txt$', TemplateView.as_view(
    	template_name='robots.txt', content_type='text/plain')),
    	
    # Admin site
    url(r'^administr8/', admin.site.urls),
    
    # Sub-directories redirect to child urls.py files
    url(r'^homepage/', include('homepage.urls')),
    url(r'^member/', include('manage_members.urls')),
    url(r'^payment/', include('payments.urls')),
    
    # Paypal listener (in django-paypal package)
    url(r'^paypal/', include('paypal.standard.ipn.urls')),
    
    # Auth view urls
    url(r'^accounts/login/$', auth_views.LoginView.as_view(
		template_name='accounts/login.html'), name='site_login'),
	url(r'^accounts/logout/$', auth_views.LogoutView.as_view(
		template_name='accounts/logged_out.html'), name='site_logout'),
	url(r'^accounts/password_change/$', auth_views.PasswordChangeView.as_view(
		template_name='accounts/password_change_form.html'), name='password_change'),
	url(r'^accounts/password_change/done/$', auth_views.PasswordChangeDoneView.as_view(
		template_name='accounts/password_change_done.html'), name='password_change_done'),
	url(r'^accounts/profile/$', member_views.redirect_to_profile),
	url(r'^accounts/reset_password/$', auth_views.PasswordResetView.as_view(
		template_name='accounts/password_reset_form.html'), name='password_reset'),
	url(r'^accounts/reset_password/done/$', auth_views.PasswordResetDoneView.as_view(
		template_name='accounts/password_reset_done.html'), name='password_reset_done'),
	url(r'^accounts/reset_password/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})',
		auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name='password_reset_confirm'),
	url(r'^accounts/reset_password/complete/$', auth_views.PasswordResetCompleteView.as_view(
		template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),
]
