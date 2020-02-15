
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import datetime
# Create your models here.

class Item(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(default='')
    date_posted = models.DateTimeField('date published')
    merchant = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(default='default_item.jpg')
    def __str__(self):
        return self.title

    def end_of_auction(self):
        return datetime.timedelta(days=10) + self.date_posted

    end_of_auction.admin_order_field = 'date_posted'
    #end_of_auction.boolean = True
    end_of_auction.short_description = 'When is end the of this auction?'

class Item_Pics(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='item_pics')
