from django.conf.urls import url, include
from creditcards.views import creditcardview, creditcarddeleteview

urlpatterns = [
    url(r'^$', creditcardview, name='creditcards'),
    url(r'^(?P<creditcard_id>\d+)/$', creditcardview, name='creditcardbound'),
    url(r'^(?P<creditcard_id>\d+)/delete/$',
        creditcarddeleteview,
        name='creditcarddelete'),
]
