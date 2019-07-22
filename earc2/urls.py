"""earc2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  re_path(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  re_path(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  re_path(r'^blog/', include('blog.urls'))
"""
from django.urls import path, re_path, include
from django.contrib import admin
from django.views.generic import TemplateView
from homepage import views as homepage_views
from manage_members import views as member_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', member_views.home_page, name="home_page"),
    path('robots.txt', TemplateView.as_view(
        template_name='robots.txt', content_type='text/plain')),
    
    # Admin site
    path('administr8/', admin.site.urls),
    
    # Sub-directories redirect to child urls.py files
    path('homepage/', include('homepage.urls')),
    path('member/', include('manage_members.urls')),
    path('payment/', include('payments.urls')),
    path('markdownx/', include('markdownx.urls')),
    
    # Paypal listener (in django-paypal package)
    path('paypal/', include('paypal.standard.ipn.urls')),
    
    # Auth view urls
    path('accounts/login/', auth_views.LoginView.as_view(
        template_name='accounts/login.html'), name='site_login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(
        template_name='accounts/logged_out.html'), name='site_logout'),
    path('accounts/password_change/', auth_views.PasswordChangeView.as_view(
        template_name='accounts/password_change_form.html'), name='password_change'),
    path('accounts/password_change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='accounts/password_change_done.html'), name='password_change_done'),
    path('accounts/profile/', member_views.redirect_to_profile),
    path('accounts/reset_password/', auth_views.PasswordResetView.as_view(
        template_name='accounts/password_reset_form.html',
        email_template_name = 'accounts/password_reset_email.html',
        subject_template_name = 'accounts/password_reset_subject.txt'), name='password_reset'),
    path('accounts/reset_password/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    re_path(r'^accounts/reset_password/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})',
        auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name='password_reset_confirm'),
    path('accounts/reset_password/complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),
]
