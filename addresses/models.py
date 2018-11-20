from __future__ import unicode_literals
from django.db import models
from users.models import Profile
from localflavor.us.models import USStateField


class Address(models.Model):
    name = models.CharField(max_length=100, blank=False)
    address1 = models.CharField("Address lines 1", max_length=128)
    address2 = models.CharField("Address lines 2", max_length=128, blank=True)
    city = models.CharField("City", max_length=64)
    state = USStateField("State", default='FL')
    zipcode = models.CharField("Zipcode", max_length=5)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=False)