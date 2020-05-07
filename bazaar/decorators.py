from django.core.exceptions import PermissionDenied
from django.utils import timezone
from .models import Item
from datetime import datetime


def active_auction(function):
    def wrap(request, *args, **kwargs):
        item = Item.objects.get(pk=kwargs['pk'])
        if item.end_of_auction > timezone.now():
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap