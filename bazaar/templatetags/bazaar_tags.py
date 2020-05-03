from django import template
from django.utils.dateparse import parse_datetime
from django.utils.timezone import is_aware, make_aware
from django.utils import timezone
from bazaar import models
from django.conf import settings
from django.utils.timezone import is_aware, is_naive, make_aware, make_naive
import dateutil.parser
import datetime
import decimal
register = template.Library()


@register.filter
def left_time(date):
    delta = date - timezone.now()
    if delta.days < 0:
        return 0
    if delta.days == 1:
        return "To the end left %s day" % delta.days
    minutes = int((delta.seconds % 3600)/60)
    hours = int(delta.seconds/3600)
    if delta.days < 1:
        return "To the end %s hours and %s minutes left." %(hours, minutes)
    return "To the end %s days left" %delta.days


@register.filter
def number_of_bids(item):
    count = models.Bid.objects.filter(item=item).count()
    if (count==1):
        noun = "bid"
    else:
        noun = "bids"

    return "%s %s" %(count, noun)

@register.filter
def default_bid(price):
    new_price = round(price*decimal.Decimal(1.05), 2)
    return new_price
