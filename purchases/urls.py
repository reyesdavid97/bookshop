from django.conf.urls import url
from . import views

app_name = 'purchases'
urlpatterns = [
    url(r'^confirm/?$', views.confirm, name='confirm'),
    url(r'^checkout/?$', views.checkout, name='checkout')
]
