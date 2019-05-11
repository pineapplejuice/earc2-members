from django.conf import settings
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from helpers.utils import EmailMessageFromTemplate
from manage_members.models import Member
from payments.paypal_helpers import paypal_email_test_or_prod
from payments.models import DuesPayment


INVALID_PAYMENT = -5.0

def _extract_member_and_year_from_custom_field(input):
    parse_custom = input.split('-')
    member = Member.objects.get(pk=int(parse_custom[0]))
    membership_year = int(parse_custom[1])
    return member, membership_year

def _email_address_is_valid(ipn_obj):
    return ipn_obj.receiver_email == paypal_email_test_or_prod()

def _payment_is_dues_payment(ipn_obj):
    return ipn_obj.item_number in ['RENEW', 'NEWQ1', 'NEWQ2', 'NEWQ3', 'NEWQ4']

def _dues_amount(item_number):
    if item_number == "RENEW":
        return 20.0
    elif item_number[0:3] == "NEW":
        return 5.0 * (5 - int(item_number[-1]))
    else:
        return INVALID_PAYMENT

def _dues_payment_is_valid(ipn_obj):
    """
    Validates payment: checks if email address matches that sent, 
    that payment is a dues payment, and amount matches.
    """
    return (_email_address_is_valid(ipn_obj)
            and _payment_is_dues_payment(ipn_obj)
            and ipn_obj.mc_gross == _dues_amount(ipn_obj.item_number)
            and ipn_obj.mc_currency == 'USD')


def show_me_the_money(sender, **kwargs):
    ipn_obj = sender
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        
        if not _dues_payment_is_valid(ipn_obj):
            return
            
        member, membership_year = \
            _extract_member_and_year_from_custom_field(ipn_obj.custom)

        DuesPayment(
            payment_date = ipn_obj.payment_date,
            membership_year = membership_year,
            member = member,
            dues_type = ipn_obj.item_number,
            payment_method = 'PP',
            ref_number = ipn_obj.txn_id,
            amount = ipn_obj.mc_gross,
        ).save()
        
        # Send email to user
        EmailMessageFromTemplate(
            subject_template = (
                'payments/subject_new_member.txt'
                    if ipn_obj.item_number[:3] == 'NEW'
                    else 'payments/subject_renewal.txt'),
            message_template = (
                'payments/email_new_member.txt'
                    if ipn_obj.item_number[:3] == 'NEW'
                    else 'payments/email_renewal.txt'),
            context = {
                'member': member,
                'amount': amount,
                'payment_date': payment_date,
            },
            recipients = [member.email_address],
            cc = settings.MEMBERSHIP_ADMINS
        ).send()
        
    else:
        return

valid_ipn_received.connect(show_me_the_money)