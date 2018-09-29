#carts/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from books.models import Book
from .cart import Cart
from .models import savedItems
from .forms import CartAddBookForm

@require_POST
def cart_add(request, book_id):
    cart = Cart(request)
    book = get_object_or_404(Book, id=book_id)
    form = CartAddBookForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(book=book,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])

    return redirect('carts:detail')

def cart_remove(request, book_id):
    cart = Cart(request)
    book = get_object_or_404(Book, id=book_id)
    cart.remove(book)
    return redirect('carts:detail')

def save_for_later(request,book_id):
    cart = Cart(request)
    book = get_object_or_404(Book, id=book_id)

    saved_book = savedItems()
    saved_book.book = book
    saved_book.save()

    cart.remove(book)
    #all_saved_books = savedItems.objects.all()
    #return render(request, 'carts:detail' , {'all_saved_books':all_saved_books})
    return redirect('carts:detail')

def delete_from_saved(request, savedItems_id):
    saved_book = get_object_or_404(savedItems, id=savedItems_id)
    saved_book.delete()
    return redirect('carts:detail')

def move_to_cart(request, savedItems_id):
    cart = Cart(request)
    saved_book = get_object_or_404(savedItems, id=savedItems_id)
    book = saved_book.book
    cart.add(book)
    saved_book.delete()

    return redirect('carts:detail')


def detail(request):
    cart = Cart(request)
    all_saved_books = savedItems.objects.all()

    for item in cart:
        item['update_quantity_form'] = CartAddBookForm(initial={'quantity': item['quantity'],
                                                                       'update': True})

    return render(request, 'cart/shopping_cart.html', {'cart' : cart, 'all_saved_books':all_saved_books})
