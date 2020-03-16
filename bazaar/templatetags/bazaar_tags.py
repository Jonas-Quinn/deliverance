from django import template
from django.utils import timezone

import datetime
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

