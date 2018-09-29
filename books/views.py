# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import Http404, HttpResponse, HttpResponseBadRequest
from django.db.models import Count, Avg
from django.shortcuts import render
from django.views import generic
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from carts.forms import CartAddBookForm
from django.contrib import messages
from .models import Author, Book, Review, Genre
from purchases.models import Purchase

import math
import json


class AllAuthorsView(generic.TemplateView):
    template_name = 'book_author_list.html'

    def get_context_data(self, **kwargs):
        context = super(AllAuthorsView, self).get_context_data(**kwargs)
        context['a'] = Author.objects.filter(name__startswith="A")
        context['b'] = Author.objects.filter(name__startswith="B")
        context['c'] = Author.objects.filter(name__startswith="C")
        context['d'] = Author.objects.filter(name__startswith="D")
        context['e'] = Author.objects.filter(name__startswith="E")
        context['f'] = Author.objects.filter(name__startswith="F")
        context['g'] = Author.objects.filter(name__startswith="G")
        context['h'] = Author.objects.filter(name__startswith="H")
        context['i'] = Author.objects.filter(name__startswith="I")
        context['j'] = Author.objects.filter(name__startswith="J")
        context['k'] = Author.objects.filter(name__startswith="K")
        context['l'] = Author.objects.filter(name__startswith="L")
        context['m'] = Author.objects.filter(name__startswith="M")
        context['n'] = Author.objects.filter(name__startswith="N")
        context['o'] = Author.objects.filter(name__startswith="O")
        context['p'] = Author.objects.filter(name__startswith="P")
        context['q'] = Author.objects.filter(name__startswith="Q")
        context['r'] = Author.objects.filter(name__startswith="R")
        context['s'] = Author.objects.filter(name__startswith="S")
        context['t'] = Author.objects.filter(name__startswith="T")
        context['u'] = Author.objects.filter(name__startswith="U")
        context['v'] = Author.objects.filter(name__startswith="V")
        context['w'] = Author.objects.filter(name__startswith="W")
        context['x'] = Author.objects.filter(name__startswith="X")
        context['y'] = Author.objects.filter(name__startswith="Y")
        context['z'] = Author.objects.filter(name__startswith="Z")

        return context


def search(request):
    books = Book.objects.all().order_by("title")
    q = request.GET.get('q')
    if q:
        books = books.filter(title__icontains=q) | \
            books.filter(author__name__icontains=q) | \
            books.filter(genre__name__icontains=q)
        return render(request, 'book_search.html', {'books': books, 'query': q})
    return HttpResponse('Please submit a search term.')


def book_list(request):
    all_books = Book.objects.all().order_by("title")
    paginator = Paginator(all_books, 12)
    page = request.GET.get('page')
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)

    index = books.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 5 if index >= 5 else 0
    end_index = index + 5 if index <= max_index - 5 else max_index
    page_range = paginator.page_range[start_index:end_index]

    context = {
        'page': page,
        'books': books,
        'all_books': all_books,
        'page_range': page_range
    }

    return render(request, 'book_list.html', context)


def book_detail(request, book_id):
    try:
        book = Book.objects.get(pk=book_id)

        # Add books to the shopping cart
        cart_book_form = CartAddBookForm()

        # reviews
        reviews = book.review_set.all().order_by('-created_at')
        reviews_count = book.review_set.count()

        avg_rating = book.review_set.aggregate(Avg('rating'))['rating__avg']
        rating_count = book.review_set.aggregate(
            Count('rating'))['rating__count']

        if rating_count > 0:
            range_pos = int(math.floor(avg_rating))
            rating_filled = range(range_pos)
            rating_empty = range(5 - range_pos)
        else:
            rating_filled = None
            rating_empty = None

        review_allowed = can_review_book(request, book)

        templ_context = {
            'book': book,
            'cart_book_form': cart_book_form,
            'review_objs': get_review_stats(reviews),
            'reviews_count': reviews_count,
            'rating_filled': rating_filled,
            'rating_empty': rating_empty,
            'avg_rating': avg_rating,
            'rating_count': rating_count,
            'review_allowed': review_allowed
        }

    except Book.DoesNotExist:
        raise Http404("Book does not exist")
    return render(request, 'book_detail.html', templ_context)


def author_list(request, author_id):
    try:
        author = Author.objects.get(pk=author_id)
        book_list = Book.objects.all().filter(author=author)
        context = {'author': author, 'book_list': book_list}
    except Author.DoesNotExist:
        raise Http404("Author does not exist")
    return render(request, 'book_author.html', context)


def genre_list(request, genre_id):
    try:
        genre = Genre.objects.get(pk=genre_id)
        book_list = Book.objects.all().filter(genre=genre)
        context = {'genre': genre, 'book_list': book_list}
    except Genre.DoesNotExist:
        raise Http404("Genre does not exist")
    return render(request, 'book_genre.html', context)


def book_genre(request):
    genre_list = Genre.objects.all()
    context = {'genres': genre_list}

    return render(request, 'book_genre_list.html', context)


def book_review(request, book_id):
    if request.is_ajax():
        try:
            if request.method == 'POST':
                user = request.user
                book_id = book_id
                review_data = json.loads(request.body)
                # print book_id, user, review_data
                if not review_data['rating'] and not review_data['comments']:
                    raise Exception("Need rating or comment")
                review = create_review(
                    book_id,
                    user,
                    review_data['rating'],
                    review_data['comments'],
                    review_data['anonymous']
                )
                review.save()
                messages.add_message(request, messages.INFO,
                                     'Your review was saved!')
                return HttpResponse("Saved")
        except Exception as inst:
            return HttpResponseBadRequest(inst)
    return HttpResponse("OK")

# Helpers


def can_review_book(request, book):
    if request.user.is_authenticated:
        # check if have purchase
        user = request.user
        try:
            purchases = Purchase.objects.filter(user=user, book=book)
            return len(purchases) > 0
        except Purchase.DoesNotExist:
            print("purchase not found")
            return False
    else:
        return False


def create_review(book_id, user, rating, comments, anonymous):
    book = Book.objects.get(pk=book_id)
    incognito = False
    if anonymous:
        incognito = anonymous
    if rating == 0:
        rating = None
    review = Review(book=book, author=user, rating=rating,
                    comments=comments, anonymous=incognito)
    return review


def get_review_stats(reviews):
    aggs = []
    for review in reviews:
        if review.rating == None:
            aggs.append((review, None))
        else:
            aggs.append((review, {
                "filled": range(review.rating),
                "empty": range(5 - review.rating)
            }))
    return aggs
