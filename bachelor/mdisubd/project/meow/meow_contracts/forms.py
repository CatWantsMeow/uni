from django import forms


class RentRequestForm(forms.Form):

    description = forms.CharField(
        max_length=300, required=False, help_text='Some info',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Description',
                'rows': 5,
            }
        )
    )


class RentContractForm(forms.Form):

    code = forms.IntegerField(
        required=True, help_text='Code of rent contract',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Code'
            }
        )
    )

    start_date = forms.DateField(
        required=True, help_text='Date when rent starts',
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Start date',
            }
        )
    )

    end_date = forms.DateField(
        required=True, help_text='Date when rent ends',
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'End date',
            }
        )
    )

    price = forms.FloatField(
        required=True, help_text='Price for month of rent',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Price'
            }
        )
    )

    additional_payment = forms.FloatField(
        required=True, help_text='Some additional payment',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Additional payment'
            }
        )
    )

    discount = forms.FloatField(
        required=True, help_text='Discount',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Discount'
            }
        )
    )

    checking_account = forms.IntegerField(
        required=True, help_text='Checking account',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Checking account'
            }
        )
    )

    requirements = forms.CharField(
        max_length=300, required=True, help_text='Requirements of the contract',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Requirements',
                'rows': 5,
            }
        )
    )

