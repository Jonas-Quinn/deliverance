from django.db import models
from django.contrib.auth.models import User
from bazaar.models import Item

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_joined = models.DateTimeField('date joined', auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} Profile'