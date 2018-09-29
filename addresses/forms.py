import re
from django import forms
from django_countries.widgets import CountrySelectWidget
from localflavor.us.forms import USStateSelect

from addresses.models import Address


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['name', 'address1', 'address2', 'city', 'state', 'zipcode']

    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['address1'].required = True
        self.fields['city'].required = True
        self.fields['state'].required = True
        self.fields['zipcode'].required = True

        self.fields['name'].widget.attrs[
            'placeholder'] = 'Shipping address familiar name'
        self.fields['address1'].widget.attrs['placeholder'] = 'Address 1'
        self.fields['address2'].widget.attrs['placeholder'] = 'Address 2'
        self.fields['city'].widget.attrs['placeholder'] = 'City'
        self.fields['zipcode'].widget.attrs['placeholder'] = 'Zip Code'

    def clean(self):
        self.error_messages = []

        # Street trying to cover all the possibilities
        street = self.cleaned_data['address1'].lower()
        pattern = re.compile(
            r'\d+[ ](?:[A-Za-z0-9.-]+[ ]?)+(?:avenue|lane|road|boulevard|drive|street|ave|dr|rd|blvd|ln|st|west|east|north|south|n|s|w|e|way|ct|ter)\.?'
        )
        if not pattern.match(str(street)):
            self.error_messages.append('Wrong format in line address 1')
            self._errors['street'] = 'Please enter a valid street address'

        # City Assuming that the city name starts with a letter
        city = self.cleaned_data['city'].lower()
        pattern = re.compile(r'([A-Za-z0-9]+\s)*')
        if not pattern.match(str(city)):
            self.error_messages.append('Wrong format in city field')
            self._errors['city'] = 'Please enter a valid city name'

        # Zip code only 5 digits
        zipcode = self.cleaned_data['zipcode']
        pattern = re.compile(r'^[0-9]{5}$')
        if not pattern.match(str(zipcode)):
            self.error_messages.append('Wrong zipcode format')
            self._errors['zipcode'] = 'Please enter a valid zipcode(5 digits)'

        if len(self.error_messages):
            self.error_message = ' & '.join(self.error_messages)
            raise forms.ValidationError(' & '.join(self.error_messages))

        return self.cleaned_data


class DeleteAddressConfirmation(forms.Form):
    pass