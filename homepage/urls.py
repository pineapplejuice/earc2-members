from django.urls import path, re_path
from . import views


urlpatterns = [
    path('about/', views.about, name="about"),
    path('antennas/', views.antennas, name="antennas"),
    path('antennas/success/', views.antenna_purchase_completed, 
        name="antenna_purchase_completed"),
    path('antennas/cancelled/', views.antenna_purchase_cancelled,
        name="antenna_purchase_cancelled"),
    path('contact/', views.contact, name="contact"),
    path('contact/success/', views.contact_success, name="contact_success"),
    path('events/', views.this_month, name="events"),
    path('events/<int:id>/', views.view_event, name="view_event"),
    path('events/calendar/<int:year>/<int:month>/', views.calendar, name="event_calendar"),
    path('faq-list/', views.faq_list, name="faq_list"),
    path('field-day/', views.field_day, name="field_day"),
    path('links/', views.links, name="links"),
    path('meetings/', views.meetings, name="meetings"),
    path('nets/', views.nets, name="nets"),
    path('nh6wi/', views.nh6wi, name="nh6wi"),
    path('officers/', views.officers, name="officers"),
    path('repeaters/', views.repeaters, name="repeaters"),
    path('repeaters/allmon/', views.allmon, name="allmon"),
    path('repeaters/brandmeister/', views.brandmeister, name="brandmeister"),
    path('repeaters/logbook/', views.logbook, name="logbook"),
    path('repeaters/rules/', views.repeater_rules, name="repeater_rules"),
    path('swap-shop/', views.swap_and_shop, name="swap_and_shop"),
]
