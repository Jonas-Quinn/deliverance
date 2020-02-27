
from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages
import datetime
from django.core.validators import MinValueValidator
# from storages.backends.s3boto3 import S3Boto3Storage

import uuid
import os
def path_and_rename(prefix, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid1().hex, ext)
    return os.path.join(prefix, filename)


def get_path_for_my_model_file(instance, filename):
    return path_and_rename('auction_images/', filename)


class Item(models.Model):
    merchant      = models.ForeignKey(User, on_delete=models.CASCADE)  # , null=True, blank=True
    title         = models.CharField(max_length=200)
    description   = models.TextField(default='')
    date_posted   = models.DateTimeField('date published', auto_now_add=True)

    price         = models.DecimalField(
        'price', max_digits=8, decimal_places=2, default=0,
        validators=[MinValueValidator(0, "Are you OK?! Price can\'t be lesser than %(limit_value)s!")]
    )

    def __str__(self):
        return self.title

    def file_name(self, filename):
        extension = filename.split('.')[-1]
        return 'auction_images/%s/main_image.%s' % (self.id, extension)

    main_image = models.ImageField(
        # 'main image', default='heroes3.png', upload_to=file_name, storage=S3Boto3Storage()
        'main image', default='default_item.jpg', upload_to=get_path_for_my_model_file
        # 'main image', default='default_item.jpg', upload_to=file_name
    )


    def get_absolute_url(self):
        return reverse('item-detail', kwargs={'pk': self.pk})

    def end_of_auction(self):
        return datetime.timedelta(days=10) + self.date_posted

    end_of_auction.admin_order_field = 'date_posted'
    #end_of_auction.boolean = True
    end_of_auction.short_description = 'When is end the of this auction?'
#
# def upload_images_location(instance, filename):
#     filebase, extension = filename.split('.')
#     return 'auction_images/%s/%s.%s' % (instance.item.id, instance.id, extension)

class Item_Image(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.item.id)

    # def file_name(self, filename):
    #     extension = filename.split('.')[-1]
    #     return 'auction_images/%s/%s.%s' % (self.item.id, self.id, extension)

    image = models.ImageField(upload_to=get_path_for_my_model_file, default='default_item.jpg')

    # problem with this feature in S3
    # def save(self, *args, **kwargs):
    #     super().save(*args,**kwargs)
    # #
    #     img = Image.open(self.image.path)
    #
    #     if img.height > 800 or img.width > 800:
    #         output_size = (800, 800)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)


