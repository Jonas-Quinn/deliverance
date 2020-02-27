# from django.db.models.signals import post_save
#
# from django.contrib.auth.models import User
# from django.dispatch import receiver
# from .models import Item, Item_Image
#
# @receiver(post_save, sender=Item)
# def create_item_image(sender, instance, created, **kwargs):
#     if created:
#         Item_Image.objects.create(Item_Image=instance)
#
# @receiver(post_save, sender=Item)
# def save_item_image(sender, instance, **kwargs):
#     instance.item_image.save()