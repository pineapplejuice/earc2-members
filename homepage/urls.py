from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^about/$', views.about, name="about"),
    url(r'^antennas/$', views.antennas, name="antennas"),
    url(r'^antennas/success/$', views.antenna_purchase_completed, 
        name="antenna_purchase_completed"),
    url(r'^antennas/cancelled/$', views.antenna_purchase_cancelled,
        name="antenna_purchase_cancelled"),
    url(r'^contact/$', views.contact, name="contact"),
    url(r'^contact/success/$', views.contact_success, name="contact_success"),
    url(r'^events/$', views.this_month, name="events"),
    url(r'^events/(?P<id>[0-9]+)/$', views.view_event, name="view_event"),
    url(r'^events/calendar/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.calendar, name="event_calendar"),
    url(r'^faq-list/$', views.faq_list, name="faq_list"),
    url(r'^field_day/$', views.field_day, name="field_day"),
    url(r'^links/$', views.links, name="links"),
    url(r'^meetings/$', views.meetings, name="meetings"),
    url(r'^nets/$', views.nets, name="nets"),
    url(r'^nh6wi/$', views.nh6wi, name="nh6wi"),
    url(r'^officers/$', views.officers, name="officers"),
    url(r'^repeaters/$', views.repeaters, name="repeaters"),
    url(r'^repeaters/allmon/$', views.allmon, name="allmon"),
    url(r'^repeaters/brandmeister/$', views.brandmeister, name="brandmeister"),
    url(r'^repeaters/rules/$', views.repeater_rules, name="repeater_rules"),
    url(r'^swap-shop/$', views.swap_and_shop, name="swap_and_shop"),
]
