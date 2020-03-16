# Generated by Django 2.2.6 on 2020-03-16 10:14

import bazaar.models
import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(default='')),
                ('date_posted', models.DateTimeField(auto_now_add=True, verbose_name='date published')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=8, validators=[django.core.validators.MinValueValidator(0, "Are you OK?! Price can't be lesser than %(limit_value)s!")], verbose_name='price')),
                ('end_of_auction', models.DateTimeField(default=datetime.datetime(2020, 3, 26, 10, 14, 48, 240101, tzinfo=utc), validators=[django.core.validators.MinValueValidator(datetime.datetime(2020, 3, 16, 10, 14, 48, 240137, tzinfo=utc), "You can't set end of auction in the past.")], verbose_name='end of auction')),
                ('main_image', models.ImageField(default='default_item.jpg', upload_to=bazaar.models.get_path_for_my_model_file, verbose_name='main image')),
                ('merchant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Watch_List',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('items', models.ManyToManyField(to='bazaar.Item', verbose_name='watch list')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Item_Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='default_item.jpg', upload_to=bazaar.models.get_path_for_my_model_file)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bazaar.Item')),
            ],
        ),
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bid', models.DecimalField(decimal_places=2, default=0, max_digits=8, validators=[django.core.validators.MinValueValidator(0, "Are you OK?! Price can't be lesser than %(limit_value)s!")], verbose_name='new price')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bazaar.Item')),
                ('merchant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
