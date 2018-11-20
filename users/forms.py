import re
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from users.models import Profile, User


class LogoutForm(forms.Form):
    pass


class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, label='First name')
    last_name = forms.CharField(max_length=30, label='Last name')
    email = forms.EmailField()

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email']

    def validate_non_numeric(self, str_exp):
        pattern = re.compile(r"([a-zA-Z]+)")
        if not pattern.match(str_exp):
            raise ValidationError('Field is incorrect')
        return str_exp

    def clean_first_name(self):
        return self.validate_non_numeric(self.cleaned_data['first_name'])

    def clean_last_name(self):
        return self.validate_non_numeric(self.cleaned_data['last_name'])

    def clean_email(self):
        value = self.cleaned_data['email']
        pattern = re.compile(
            r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
        if not pattern.match(value):
            raise ValidationError('Email format is incorrect')
        return value


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['nick_name', 'image']

    def clean_nick_name(self):
        value = self.cleaned_data['nick_name']

        pattern = re.compile(r"(^[a-zA-Z]*[a-zA-Z0-9-]*$)")
        if not pattern.match(value):
            raise ValidationError('Nickname format is incorrect')
        return value


class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields