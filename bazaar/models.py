
from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
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
    slug          = models.SlugField(unique=True)
    description   = models.TextField(default='')
    date_posted   = models.DateTimeField('date published', auto_now_add=True)
    price         = models.DecimalField(
        'price', max_digits=8, decimal_places=2, default=0,
        validators=[MinValueValidator(0, "Are you OK?! Price can\'t be lesser than %(limit_value)s!")]
    )
    end_of_auction = models.DateTimeField(
        'end of auction',
        default=timezone.now()+datetime.timedelta(days=10),
        validators=[MinValueValidator(
            timezone.now(),
            "You can\'t set end of auction in the past."
        )]
    )

    class Condition(models.TextChoices):
        NEW = 'NEW', _('New')
        USED = 'USE', _('Used')
        REFURBISHED = 'REF', _('Refurbished')
        NOT_WORKING = 'NOT', _('For parts or not working')

    #
    # CONDITION_CHOICES = [
    #     (NEW, 'New'),
    #     (USED, 'Used'),
    #     (REFURBISHED, 'Refurbished'),
    #     (NOT_WORKING, 'For parts or not working'),
    # ]
    condition = models.CharField(
        'condition',
        max_length=3,
        choices=Condition.choices,
        default=Condition.USED,
    )

    def __str__(self):
        return self.title

    def file_name(self, filename):
        extension = filename.split('.')[-1]
        return 'auction_images/%s/main_image.%s' % (self.id, extension)

    main_image = models.ImageField(
        # 'main image', default='heroes3.png', upload_to=file_name, storage=S3Boto3Storage()
        'thumbnail', default='default_item.jpg', upload_to=get_path_for_my_model_file
        # 'main image', default='default_item.jpg', upload_to=file_name
    )

    def get_absolute_url(self):
        return reverse('item-detail', kwargs={'slug': self.slug})

    def remaining_time(self):
        # if (self.end_of_auction - self.date_posted).days > 0:
        return ( self.end_of_auction - timezone.now() ).days

    remaining_time.admin_order_field = 'remaining_time'
    remaining_time.short_description = 'How much time is left?'

def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Item.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first.id)
        return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_item_receiver(sender, instance, *args, **kwargs):
   if not instance.slug:
       instance.slug = create_slug(instance)

pre_save.connect(pre_save_item_receiver, sender=Item)

# def upload_images_location(instance, filename):
#     filebase, extension = filename.split('.')
#     return 'auction_images/%s/%s.%s' % (instance.item.id, instance.id, extension)


class Item_Image(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_path_for_my_model_file, default='default_item.jpg')

    def __str__(self):
        return str(self.item.id)


class Bid(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='item_id')
    merchant = models.ForeignKey(User, models.SET_NULL, blank=True, null=True, related_name='user_bid_id')
    bid = models.DecimalField(
        'new price', max_digits=8, decimal_places=2, default=0,
        validators=[MinValueValidator(0, "Are you OK?! Price can\'t be lesser than %(limit_value)s!")]
    )
    date = models.DateTimeField(auto_now_add=True)


class Watch_List(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item, verbose_name="watch list")
