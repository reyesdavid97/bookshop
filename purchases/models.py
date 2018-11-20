from __future__ import unicode_literals
from django.db import models

from books.models import Book
from django.contrib.auth import settings
# Create your models here.

class Purchase(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  book = models.ForeignKey(Book, on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  def __str__(self):
    return "User: " + self.user.username + ", Book: " + self.book.title
