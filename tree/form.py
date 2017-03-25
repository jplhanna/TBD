from django import forms
from django.contrib.auth.models import User
from bootstrap_toolkit.widgets import BootstrapDateInput, BootstrapTextInput, BootstrapUneditableInput


class LoginForm(forms.Form):
    username = forms.CharField(
        required=True,
        label="Email",
        error_messages={'required': 'Please enter email'},
        widget=forms.TextInput(
            attrs={
                'placeholder': "Email",
            }
        ),
    )
    password = forms.CharField(
        required=True,
        label="Password",
        error_messages={'required': 'Please enter the password'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder': "Password",
            }
        ),
    )

    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError("Email and Password are required")
        else:
            cleaned_data = super(LoginForm, self).clean()
