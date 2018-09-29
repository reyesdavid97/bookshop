from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from addresses.models import Address
from addresses.forms import AddressForm, DeleteAddressConfirmation
from bookmart.utils import rendermessage, renderconfirmation, render_access_denied_message
from users.models import User


@login_required
def addressview(request, user_id, address_id=None):
    address = None
    addresses_list = Address.objects.all().filter(user=user_id)

    if address_id:
        try:
            address = Address.objects.get(pk=address_id)
            addresses_list = Address.objects.filter(user=user_id).exclude(
                pk=address_id)
        except:
            return rendermessage(
                request, 'Error', 'Shipping does not exist', '',
                reverse('users:addresses',
                        args=[str(user_id)]), 'shipping addresses page')

    if request.method == "POST":
        if address:
            addressform = AddressForm(request.POST, instance=address)
        else:
            addressform = AddressForm(request.POST, initial=request.POST)

        if addressform.is_valid():
            newaddress = addressform.save(commit=False)
            newaddress.user_id = user_id
            newaddress.save()
            return rendermessage(request, 'New address confirmation',
                                 'Shipping address added succefully', '',
                                 reverse(
                                     'users:addresses',
                                     args=[str(user_id)]), 'addresses page')

        return rendermessage(
            request, 'Shipping address | Error', 'Shipping address ',
            'There was an error adding the shipping address. ' +
            addressform.error_message,
            reverse('users:addresses',
                    args=[str(user_id)]), 'shipping addresses page')
    else:  # GET
        if address:
            addressform = AddressForm(instance=address)
            button_text = 'Modify shiping address'
            page_title = address.name
        else:
            addressform = AddressForm()
            button_text = 'Add new shipping address'
            page_title = 'New'

    return render(request, 'addresses/addresses.html', {
        'user_id': user_id,
        'address': address,
        'page_title': page_title,
        'form': addressform,
        'addresses_list': addresses_list,
        'button_text': button_text,
    })


@login_required
def addressdeleteview(request, user_id, address_id):

    try:
        user = User.objects.get(pk=user_id)
        address = Address.objects.get(pk=address_id)
    except:
        return render_access_denied_message(request)

    form = DeleteAddressConfirmation(request)
    if request.method == 'POST':
        form = DeleteAddressConfirmation(request.POST)
        if request.POST.get('Confirm'):
            #Confirmed deletion
            address.delete()
            return rendermessage(request, 'Delete confirmation',
                                 'Shipping address removed succefully', '',
                                 reverse(
                                     'users:addresses', args=[str(user_id)]),
                                 'shipping addresses page')
        else:
            # Cancelled deletion returned to the shippping addresses page
            return HttpResponseRedirect(
                reverse('users:addresses', args=[str(user_id)]))

    return renderconfirmation(
        request, form, 'Delete shipping address', 'Please confirm',
        'Are you sure you want to delete the shipping address?')
