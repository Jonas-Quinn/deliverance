from django import template
import datetime
register = template.Library()


@register.filter
def time_until(date):
    delta = datetime.date(date) - datetime.now().date()
    return delta.days
