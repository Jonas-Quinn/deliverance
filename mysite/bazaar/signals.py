from django.db.models.signals import post_save

from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Item, Item_Pics

@receiver(post_save, sender=Item)
def create_item_pics(sender, instance, created, **kwargs):
    if created:
        Item.objects.create(Item_Pics=instance)

@receiver(post_save, sender=Item)
def save_item_pics(sender, instance, **kwargs):
    instance.Item_Pics.save()