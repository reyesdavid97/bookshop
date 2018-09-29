from django.views.generic.list import ListView
from books.models import Book


class HomePageView(ListView):
    model = Book
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['latest_books'] = Book.objects.all().order_by('-release_date')[:8]
        return context
