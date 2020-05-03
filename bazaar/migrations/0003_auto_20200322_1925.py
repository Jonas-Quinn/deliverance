# Generated by Django 2.2.6 on 2020-03-22 18:25

import datetime
import django.core.validators
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('bazaar', '0002_auto_20200322_1925'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='end_of_auction',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 1, 18, 25, 44, 951015, tzinfo=utc), validators=[django.core.validators.MinValueValidator(datetime.datetime(2020, 3, 22, 18, 25, 44, 951028, tzinfo=utc), "You can't set end of auction in the past.")], verbose_name='end of auction'),
        ),
    ]