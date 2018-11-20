from django.conf.urls import url
from . import views

app_name = 'carts'
urlpatterns = [
    url(r'^$', views.detail, name='detail'),
    url(r'^add/(?P<book_id>\d+)/$', views.cart_add, name='add'),
    url(r'^remove/(?P<book_id>\d+)/$', views.cart_remove, name='cart_remove'),
    url(r'^save/(?P<book_id>\d+)/$', views.save_for_later, name='save_for_later'),
    url(r'^addBackToCart(?P<savedItems_id>\d+)/$', views.move_to_cart, name='move_to_cart'),
    url(r'^(?P<savedItems_id>\d+)/$', views.delete_from_saved, name='delete_from_saved')
]
