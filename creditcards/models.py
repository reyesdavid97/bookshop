from django.db import models
from users.models import Profile
from creditcards.choices import MONTHS, YEARS, JAN, THIS_YEAR


class CreditCard(models.Model):
    name = models.CharField(max_length=100, blank=False)
    number = models.CharField(max_length=16, blank=False, unique=True)
    expdate_month = models.IntegerField(choices=MONTHS, default=JAN)
    expdate_year = models.IntegerField(choices=YEARS, default=THIS_YEAR)
    securitycode = models.IntegerField(blank=False)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=False)
