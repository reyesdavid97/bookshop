import re
import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm, ChoiceField, CharField
from creditcards.choices import MONTHS, YEARS
from .models import CreditCard


class CreditCardForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CreditCardForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Credit card name'
        self.fields['number'] = forms.CharField(widget=forms.TextInput(
            attrs={'id': 'creditcard-number'}))
        self.fields['number'].widget.attrs[
            'placeholder'] = 'Credit card number'
        self.fields['expdate_month'] = ChoiceField(choices=MONTHS)
        self.fields['expdate_year'] = ChoiceField(choices=YEARS)
        self.fields['securitycode'].widget.attrs[
            'placeholder'] = 'Security code'

    class Meta:
        model = CreditCard
        fields = [
            'name', 'number', 'expdate_month', 'expdate_year', 'securitycode'
        ]

    def clean(self):
        # errors
        self.error_messages = []

        # Card number block
        number = self.cleaned_data['number']

        visa_pattern = r'^4[0-9]{12}(?:[0-9]{3})?$'
        mastercard_pattern = r'^(?:5[1-5][0-9]{2}|222[1-9]|22[3-9][0-9]|2[3-6][0-9]{2}|27[01][0-9]|2720)[0-9]{12}$'
        americanexpress_pattern = r'^3[47][0-9]{13}$'
        discover_pattern = r'^6(?:011|5[0-9]{2})[0-9]{12}$'

        patterns_list = [
            discover_pattern,
            visa_pattern,
            mastercard_pattern,
        ]
        pattern_string = '|'.join(patterns_list)

        pattern1 = re.compile(pattern_string)  #3 digits of security code
        pattern2 = re.compile(
            americanexpress_pattern)  # four digits security code

        if pattern1.match(str(number)):
            security_code_pattern = re.compile(r'^[0-9]{3}$')  # 3
        elif pattern2.match(str(number)):
            security_code_pattern = re.compile(r'^[0-9]{4}$')  # 4
        else:
            security_code_pattern = None

        if not pattern1.match(str(number)) and not pattern2.match(str(number)):
            self.error_messages.append('Credit card number not valid')
            self._errors['number'] = 'Please enter a valid credit card number'

        # Expiration date block
        month = int(self.cleaned_data['expdate_month'])
        year = int(self.cleaned_data['expdate_year'])
        expdate = datetime.datetime(year, month, 1)  # first day of the month
        today = datetime.datetime.today()

        if expdate < today:
            self.error_messages.append('Card has expired')
            self._errors[
                'expdate_month'] = 'Please verify the credit card expiration date'
            self._errors[
                'expdate_year'] = 'Please verify the credit card expiration date'

        # Security code block
        security_code = self.cleaned_data['securitycode']

        # if not security_code_pattern created or does not match the work the errors
        if not security_code_pattern or not security_code_pattern.match(
                str(security_code)):
            self.error_messages.append('Invalid security code')
            self._errors[
                'securitycode'] = 'Please verify the credit card security code'

        self.error_message = ''
        if len(self.error_messages):
            self.error_message = ' & '.join(self.error_messages)
            raise forms.ValidationError(' & '.join(self.error_messages))

        return self.cleaned_data


class DeleteCreditCardConfirmation(forms.Form):
    pass
