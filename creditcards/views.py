from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect
from creditcards.forms import CreditCardForm, DeleteCreditCardConfirmation
from creditcards.models import CreditCard
from users.models import User
from bookmart.utils import rendermessage, renderconfirmation, render_access_denied_message


@login_required
def creditcardview(request, user_id, creditcard_id=None):

    # instantiate variables
    creditcard = None
    creditcards_list = CreditCard.objects.filter(user=user_id)
    if creditcard_id:
        try:
            creditcard = CreditCard.objects.get(pk=creditcard_id)
            creditcards_list = CreditCard.objects.filter(user=user_id).exclude(
                pk=creditcard_id)
        except:
            return rendermessage(request, 'Credit Card | Error',
                                 'Credit card does not exist', '',
                                 reverse(
                                     'users:creditcards',
                                     args=[str(user_id)]), 'creditcards page')

    if request.method == "POST":
        if creditcard:
            creditcardform = CreditCardForm(request.POST, instance=creditcard)
        else:
            creditcardform = CreditCardForm(request.POST, initial=request.POST)

        if creditcardform.is_valid():
            newcreditcard = creditcardform.save(commit=False)
            newcreditcard.user_id = user_id
            newcreditcard.save()
            return rendermessage(request, 'Credit card | Confirmation',
                                 'Credit card added/updated succefully', '',
                                 reverse(
                                     'users:creditcards',
                                     args=[str(user_id)]), 'creditcards page')

        return rendermessage(request, 'Credit card | Error', 'Credit card ',
                             'There was an error processing the creditcard. ' +
                             creditcardform.error_message,
                             reverse('users:creditcards',
                                     args=[str(user_id)]), 'creditcards page')
    else:  # GET
        if creditcard:
            creditcardform = CreditCardForm(instance=creditcard)
            button_text = 'Modify credit card'
            page_title = creditcard.name
        else:
            creditcardform = CreditCardForm()
            button_text = 'Add credit card'
            page_title = 'New'

    return render(request, 'creditcards/creditcards.html', {
        'user_id': user_id,
        'creditcard': creditcard,
        'form': creditcardform,
        'page_title': page_title,
        'creditcards_list': creditcards_list,
        'button_text': button_text,
    })


@login_required
def creditcarddeleteview(request, user_id, creditcard_id):

    try:
        user = User.objects.get(pk=user_id)
        creditcard = CreditCard.objects.get(pk=creditcard_id)
    except:
        return render_access_denied_message(request)

    form = DeleteCreditCardConfirmation(request)
    if request.method == 'POST':
        form = DeleteCreditCardConfirmation(request.POST)
        if request.POST.get('Confirm'):
            #Confirmed deletion
            creditcard.delete()
            return rendermessage(request, 'Credit Card Delete | Confirmation',
                                 'Credit card removed succefully', '',
                                 reverse(
                                     'users:creditcards',
                                     args=[str(user_id)]), 'creditcards page')
        else:
            # Cancelled deletion returned to credit cards page
            return HttpResponseRedirect(
                reverse('users:creditcards', args=[str(user_id)]))

    return renderconfirmation(
        request, form, 'Delete credit card', 'Please confirm',
        'Are you sure you want to delete the credit card?')
