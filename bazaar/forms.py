from django import forms
from .models import Item_Image, Item, Bid
from django.contrib.auth.models import User
from django.forms import DateTimeField
from django.contrib.admin import widgets
from django.core.validators import ValidationError, MinValueValidator
from crispy_forms.helper import FormHelper
import datetime
import decimal

class ItemCreateForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = (
            'title',
            'description',
            'price',
            'end_of_auction',
            'condition',
            'main_image',
        )
        widgets = {
            'end_of_auction': forms.DateTimeInput( attrs={'class': 'cosmicbutton',} ),
        }

    def __init__(self, *args, **kwargs):
        super(ItemCreateForm, self ).__init__( *args, **kwargs )
        self.fields['end_of_auction'].label = ""

class ItemCreateDatetimeForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = (
            'end_of_auction',
        )


class ItemImageForm(forms.ModelForm):
    model = Item_Image

    def __init__(self, *args, **kwargs):
        super(ItemImageForm, self).__init__(*args, **kwargs)

        if 'instance' in kwargs:
            item_image = kwargs['instance']

        # to add an extra field, add something like this
        self.fields['extra_field'] = forms.CharField(max_length=30)

    class Meta:
        fields = ('image',)


class ItemEditForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = (
            'title',
            'description',
            'main_image',
        )


class BiddingForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = (
            'bid',
        )

    # here we pass old_price variable outside the form
    def __init__(self, *args, **kwargs):
        self.old_price = kwargs.pop('old_price')
        super(BiddingForm, self).__init__(*args, **kwargs)

    def clean(self):
        cd = self.cleaned_data
        if not ('bid' in cd.keys()):
            raise forms.ValidationError("Please fill out missing field.")

        new_price = cd['bid']
        if new_price < round( self.old_price*decimal.Decimal(1.05), 2):
            raise ValidationError("The new price must be at least 5% higher then the previous one.")

        return cd
