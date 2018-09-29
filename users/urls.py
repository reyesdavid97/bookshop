from django.conf.urls import url, include
from creditcards import urls as creditcards_urls
from addresses import urls as addresses_urls
from users.forms import SignUpForm
from . import views

urlpatterns = [
    url(r'^(?P<pk>\d+)/$', views.ProfileUpdateView.as_view(), name='profile'),
    url(r'^(?P<user_id>\d+)/creditcards/', include(creditcards_urls)),
    url(r'^(?P<user_id>\d+)/addresses/', include(addresses_urls)),
    url(r'^(?P<user_id>\d+)/changepassword/$',
        views.changepassword,
        name='changepassword'),
    url(r'logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'signup/$',
        views.SignUpView.as_view(form_class=SignUpForm),
        name='signup'),
    url('^', include('django.contrib.auth.urls'))
]
