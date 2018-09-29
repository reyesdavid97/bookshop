from django.conf.urls import url
from addresses.views import addressview, addressdeleteview
from . import views

urlpatterns = [
    url(r'^$', addressview, name='addresses'),
    url(r'^(?P<address_id>\d+)/$', addressview, name='addressbound'),
    url(r'^(?P<address_id>\d+)/delete/$',
        addressdeleteview,
        name='addressdelete'),
]
