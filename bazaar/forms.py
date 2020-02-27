from django import forms
from .models import Item_Image, Item
from django.contrib.auth.models import User

class ItemCreateForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = (
            'title',
            'description',
            'price',
            'main_image',
        )

class ItemEditForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = (
            'title',
            'description',
            'main_image',
        )
