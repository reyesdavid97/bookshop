from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from users import urls as user_urls
from books import urls as book_urls
from carts import urls as cart_urls
from purchases import urls as purchases_urls
from bookmart.views import HomePageView
from bookmart.utils import wrong_url

urlpatterns = [
    url(r'^resetpassword/$', auth_views.password_reset,
        {'template_name': 'registration/resetpassword.html'}),
    url(r'^password_reset/done/$', auth_views.password_reset_done,
        {'template_name': 'registration/resetpassworddone.html'}),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm,
        {'template_name': 'registration/resetpasswordconfirm.html'}),
    url(r'^reset/done/$', auth_views.password_reset_complete,
        {'template_name': 'registration/resetpasswordcomplete.html'}),
    url(r'^admin/', admin.site.urls),
    url(r'^users/', include(user_urls, namespace='users')),
    url(r'^carts/', include(cart_urls)),
    url(r'^purchases/', include(purchases_urls)),
    url(r'^books/', include(book_urls)),
    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT
                                         }),
    url(r'.*', wrong_url),
] + static(
    settings.STATIC_URL, document_root=settings.STATIC_ROOT)
