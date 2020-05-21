from django import forms
from .models import Item_Image, Item, Bid
from django.contrib.auth.models import User
from django.forms import DateTimeField
from django.contrib.admin import widgets
from django.core.validators import ValidationError, MinValueValidator
from django.utils.safestring import mark_safe
from crispy_forms.helper import FormHelper
import datetime
import decimal
import math

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
            'title': forms.TextInput(
                attrs={'style': 'width: 100%; background: rgba(235, 255, 87, 0.6);', } ),
            'description': forms.Textarea(
                attrs={'style': 'width: 100%; background: rgba(235, 255, 87, 0.6);', } ),
            'price': forms.NumberInput(
                attrs={'style': 'width: 200px; background: rgba(235, 255, 87, 0.6);', } ),
            'end_of_auction': forms.DateTimeInput(
                attrs={'class': 'cosmicbutton','style': 'background: rgba(235, 255, 87, 0.6);',} ),
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
        limit = round(
            max(decimal.Decimal(0.01), math.ceil(self.old_price*decimal.Decimal(105))/100),2
        )
        if math.ceil(new_price*decimal.Decimal(100))/100 < limit:
            raise ValidationError(mark_safe("The new price must be at least 5% higher then the previous one. <br />"
                                  "The lowest possible bid: ${0}, your bid: ${1}. <br />"
                                            " Draw conclusions.".format(limit, new_price)))

        return cd

