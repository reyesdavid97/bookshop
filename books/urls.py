from django.conf.urls import url, include
from . import views
from users import urls as users_urls

app_name = 'books'
urlpatterns = [
    # /books/  this will show a page with all the Books
    url(r'^$', views.book_list, name='index'),
    url(r'^search/?$', views.search, name='search_results'),

    # /books/genre/5/ this will show a page with the list of books in genre
    url(r'^genres/$', views.book_genre, name="books_genres"),
    url(r'genres/(?P<genre_id>[0-9]+)/$',
        views.genre_list,
        name='genre_books'),

    # /books/author/5/ this will show a page with the details of the author
    url(r'^authors/$', views.AllAuthorsView.as_view(), name="books_authors"),
    url(r'author/(?P<author_id>[0-9]+)/$',
        views.author_list,
        name='author_books'),

    # /books/5/ this will show a page with the details of the book
    url(r'(?P<book_id>[0-9]+)/$', views.book_detail, name='detail'),
    url(r'(?P<book_id>[0-9]+)/review$', views.book_review, name='review'),
]
