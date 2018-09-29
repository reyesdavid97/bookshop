# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from carts.cart import Cart
from books.models import Book
from purchases.models import Purchase
from django.contrib import messages

# Create your views here.
@login_required
def confirm(request):
    cart = Cart(request)
    ctx = {'cart': cart}
    return render(request, 'purchase/confirm.html', ctx)


@login_required
def checkout(request):
    cart = Cart(request)
    books_in_cart = cart.get_books()
    user = request.user
    if len(books_in_cart) == 0:
        return redirect('home')

    for book in books_in_cart:
        purchase = Purchase(user=user, book=book)
        purchase.save()

    cart.remove_many(books_in_cart)

    ctx = {'books': books_in_cart}
    return render(request, 'purchase/finish.html', ctx)

    
