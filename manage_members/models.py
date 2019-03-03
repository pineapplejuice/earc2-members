from django.db import models
from django.db.models import signals, Max
from django.utils.timezone import now
from django.contrib.auth.models import User
import datetime


# Create your models here.

# Dropdown lists

from helpers.models import DUES_TYPE

LICENSE_TYPES = [
    ('T', 'Technician'),
    ('G', 'General'),
    ('A', 'Advanced'),
    ('E', 'Amateur Extra'),
]

TITLES = [
    ('PR', 'President'),
    ('VP', 'Vice-President'),
    ('SE', 'Secretary'),
    ('TR', 'Treasurer'),
    ('DI', 'Director'),
]

# Helper functions
def update_user(sender, instance, created, **kwargs):
    """Updates username and user demographics when member model changes"""
    if not created:
        if instance.user:           
            user = instance.user
            user.username = instance.callsign.lower()
            user.email = instance.email_address
            user.first_name = instance.first_name
            user.last_name = instance.last_name
            user.save()


class Member(models.Model):
    callsign = models.CharField(max_length=6)
    license_type = models.CharField(
        max_length=1, 
        choices=LICENSE_TYPES, 
        blank=True)
    expiration_date = models.DateField(
        verbose_name = "My license expires",
        blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=95)
    city = models.CharField(max_length=35)
    state = models.CharField(max_length=2)
    zip_code = models.CharField(max_length=10)
    phone = models.CharField(max_length=15)
    email_address = models.EmailField()
    mailing_list = models.BooleanField(
        verbose_name = "Add me to the club mailing list"
    )
    wd_online = models.BooleanField(
        verbose_name = "I would like to read the Wireless Dispatch online"
    )
    arrl_member = models.BooleanField(
        verbose_name = "I am an ARRL member"
    )
    need_new_badge = models.BooleanField(
        verbose_name = "I need a new membership badge"
    )
    position = models.CharField(max_length=2, choices=TITLES, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, 
        blank=True)
    
    
    def __str__(self):
        return self.first_name + ' ' + self.last_name + ', ' + self.callsign
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('member_profile', args=[str(self.id)])
        
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
        
    def last_dues_payment(self):
        d = self.duespayment_set.aggregate(latest_payment=Max('payment_date'))
        return d['latest_payment']
    
    def membership_expires(self):
        if self.duespayment_set.count() == 0:
            return None
        else:
            d = self.duespayment_set.aggregate(
                latest_year=Max('membership_year'))
            return datetime.date(d['latest_year'], 12, 31)
    
    def membership_status(self):
        
        # Today's date
        _today = datetime.date.today()
        
        if self.duespayment_set.count() == 0:
            return "P"  # Prospective member - no dues yet
        elif self.membership_expires() >= _today:
            return "C"  # Current member
        elif self.membership_expires().year > _today.year - 1:
            return "LR" # Lapsed member, can renew
        else:
            return "LN" # Lapsed member over a year, must join new

    def member_dues_type(self):
        if self.membership_status() in ['P', 'LN']:
            return 'NEWQ' + str((datetime.date.today().month - 1) // 3 + 1)
        else:
            return 'RENEW'
    
    def member_dues_description(self):
        return dict(DUES_TYPE)[self.member_dues_type()]
    
    def member_dues_amount(self):
        if self.membership_status() in ['C', 'LR']:
            return 20
        else:
            return 5 * (4 - (datetime.date.today().month - 1) // 3)

    def member_dues_year(self):
        # If current, renew for the year after expiration. 
        # If new or lapsed, renew for this year.
        if self.membership_status() == 'C':
            return self.membership_expires().year + 1
        else:
            return datetime.date.today().year


signals.post_save.connect(update_user, sender=Member)