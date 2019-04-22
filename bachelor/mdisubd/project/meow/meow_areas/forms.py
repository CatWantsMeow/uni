from django import forms
from meow_areas.db import get_locations, get_prices
from meow_auth.db import get_landlords
from meow_main.db import e


class ShoppingMallForm(forms.Form):

    name = forms.CharField(
        max_length=100, required=True,
        help_text='Name of shopping mall',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Name',
            }
        )
    )

    location_id = forms.ChoiceField(
        choices=[
            (l[0], "{}, {}, {}".format(l[3].encode('utf-8'), l[4].encode('utf-8'), l[5]))
            for l in get_locations()
        ],
        required=True,
        help_text='Location of shoping mall',
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'placeholder': 'Location',
            }
        )
    )

    description = forms.CharField(
        max_length=300, required=True, help_text='Some info about shopping mall',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Description',
                'rows': 5,
            }
        )
    )

    floors_number = forms.IntegerField(
        required=True, help_text='Number of floors in shopping mall',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Number of floors'
            }
        )
    )

    parking_size = forms.IntegerField(
        required=True, help_text='Parking size of shopping mall',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Parking size'
            }
        )
    )


class ShoppingAreaForm(forms.Form):

    description = forms.CharField(
        max_length=300, required=True, help_text='Some info about shopping area',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Description',
                'rows': 5,
            }
        )
    )

    area = forms.FloatField(
        required=True, help_text='Area of shopping area',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Area'
            }
        )
    )

    price_id = forms.ChoiceField(
        choices=[
            (p[0], p[1])
            for p in get_prices()
        ],
        required=True,
        help_text='Rent price of shopping area',
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'placeholder': 'Price',
            }
        )
    )

    landlord_id = forms.ChoiceField(
        choices=[
            (l[0], "{}  {}  {} ({}, {})".format(e(l[7]), e(l[8]), e(l[9]), e(l[10]), e(l[11])))
            for l in get_landlords()
        ],
        required=True,
        help_text='Landlord of shopping area',
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'placeholder': 'Landlord',
            }
        )
    )



