from django import forms


class LoginForm(forms.Form):

    username = forms.CharField(
        max_length=100, required=True, help_text='Username',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Username',
            }
        )
    )

    password = forms.CharField(
        max_length=100, required=True, help_text='Password',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Password',
                'type': 'password',
            }
        )
    )


class RegistrationForm(forms.Form):

    help_texts = {
        'username': 'Username',
        'password': 'Password',
        'email': 'Your email',
        'first_name': 'Your first name',
        'last_name': 'Your last name',
    }

    username = forms.CharField(
        max_length=200, required=True, help_text='Username',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Username',
            }
        ),
    )

    password = forms.CharField(
        max_length=200, required=True, help_text='Password',
        widget = forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Password'
            }
        ),
    )

    email = forms.CharField(
        max_length=200, required=True, help_text='Your email',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Email',
            }
        ),
    )

    first_name = forms.CharField(
        max_length=100, required=True, help_text='Your first name',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'First name',
            }
        ),
    )

    middle_name = forms.CharField(
        max_length=100, required=False, help_text='Your middle name',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Middle name',
            }
        )
    )

    last_name = forms.CharField(
        max_length=100, required=True, help_text='Your last name',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Last name',
            }
        )
    )

    phone = forms.CharField(
        max_length=30, required=True, help_text='Your phone',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Phone',
            }
        )
    )


class LandlordRegistrationForm(RegistrationForm):

    organization_name = forms.CharField(
        max_length=100, required=True, help_text='Your organization name',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Organization name',
            }
        )
    )

    description = forms.CharField(
        max_length=200, required=True, help_text='Detail information about you',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Detail Info',
                'rows': 3,
            }
        )
    )


class TenantRegistrationForm(RegistrationForm):

    requisites = forms.CharField(
        max_length=200, required=True, help_text='Your requisites',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Requisites',
            }
        )
    )