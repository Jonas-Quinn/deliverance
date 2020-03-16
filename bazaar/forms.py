from django import forms
from .models import Item_Image, Item, Bid
from django.contrib.auth.models import User
from django.forms import DateTimeField
from django.contrib.admin import widgets
from django.core.validators import ValidationError, MinValueValidator
import datetime

class DateInput(forms.DateTimeInput):
    input_type = 'date'


class TimeInput(forms.TimeInput):
    input_type = 'time'


class ItemCreateForm(forms.ModelForm):
    # end_of_auction_date = forms.DateField()
    # end_of_auction_time = forms.TimeField()
    class Meta:
        model = Item
        fields = (
            'title',
            'description',
            'price',
            'end_of_auction',
            'main_image',
        )
        widgets = {'end_of_auction': DateInput(
            attrs={ 'type': 'date'},
            format='%d-%m-%Y %H:%M')}


    # def __init__(self, *args, **kwargs):
    #     super(ItemCreateForm, self).__init__(*args, **kwargs)
    #
    #     if kwargs['instance']:
    #         self.fields['end_of_auction_date'].initial = kwargs['instance'].end_of_auction.date()
    #         self.fields['end_of_auction_time'].initial = kwargs['instance'].end_of_auction.time()
    #
    # def save(self, commit=True):
    #     model = super(ItemCreateForm, self).save(commit=False)
    #     model.end_of_auction = datetime.combine(self.cleaned_data['end_of_auction_date'], self.cleaned_data['end_of_auction_time'])
    #     if commit:
    #         model.save()
    #
    #     return model


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
        if new_price <= self.old_price:
            raise ValidationError("The new price must be at least 5% higher then previous.")

        return cd
