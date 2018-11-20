from __future__ import unicode_literals
from django.db import models
from django.contrib.auth import settings
from books.models import Book
# Create your models here.

class savedItems(models.Model):
    book = models.ForeignKey(Book, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.book.title
