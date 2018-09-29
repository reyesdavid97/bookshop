from django.shortcuts import render
from django.urls import reverse


def rendermessage(request, title, header, message, url, page_name):
    """
    Show a page with a mesage and a redirecting url
    """
    return render(request, 'user_message.html', {
        'page_title': title,
        'page_header': header,
        'page_message': message,
        'url_to_redirect': url,
        'returning_page_name': page_name
    })


def renderconfirmation(request, form, title, question_header, question_body):
    """
    Shows a page with two buttons
    """
    return render(request, 'confirmation.html', {
        'form': form,
        'page_title': title,
        'question_header': question_header,
        'question_body': question_body
    })


def render_access_denied_message(request):
    """
    Shows page with an acces denied msg
    """
    return rendermessage(request, 'Error', 'Access denied',
                         'Contact the administrator',
                         reverse('home'), 'home page')


def wrong_url(request):
    """
    To be used when no url was matched
    """
    return rendermessage(request, 'Error', 'Url not found',
                         'Please revise the url', reverse('home'), 'home page')


"""def generic_model_view(request,
                       user_id,
                       current_model,
                       model_name_str,
                       model_Form,
                       template_name,
                       succeful_url,
                       current_item_id=None):

    # instantiate variables
    current_item = None
    current_model_list = current_model.objects.filter(user=user_id)
    if current_item_id:
        try:
            current_item = current_model.objects.get(pk=current_item_id)
            current_model_list = current_model.objects.filter(
                user=user_id).exclude(pk=current_item_id)
        except:
            current_item = None

    if request.method == "POST":
        if current_item:
            current_item_form = model_Form(request.POST, instance=current_item)
        else:
            current_item_form = model_Form(request.POST, initial=request.POST)

        if current_item_form.is_valid():
            new_model_item = current_item_form.save(commit=False)
            new_model_item.user_id = user_id
            new_model_item.save()
            return rendermessage(request, model_name_str + ' confirmation',
                                 model_name_str + ' added succefully', '',
                                 succeful_url, model_name_str + ' page')

    else:  # GET
        if current_item:
            current_item_form = model_Form(instance=current_item)
            button_text = 'Modify ' + model_name_str
        else:
            current_item_form = model_Form()
            button_text = 'Add ' + model_name_str

    return render(request, template_name, {
        'user_id': user_id,
        'current_item': current_item,
        'form': current_item_form,
        'model_name_str': model_name_str,
        'current_model_list': current_model_list,
        'succeful_url': succeful_url,
        'button_text': button_text,
    })
"""