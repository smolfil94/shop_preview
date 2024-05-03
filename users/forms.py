from django import forms
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from .models import Address, User


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Email'})
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Last Name'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'})
    )

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')


class UserLoginForm(forms.Form):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Email'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone_number')


class AddressForm(forms.ModelForm):

    class Meta:
        model = Address
        fields = ('country', 'state', 'city', 'zip_code', 'address_line_1', 'address_line_2')


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Current Password", widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    # Добавьте остальные поля и настройки, если необходимо

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавьте дополнительные настройки полей, если необходимо

