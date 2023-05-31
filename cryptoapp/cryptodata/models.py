from django.contrib.auth.models import User
from django.db import models

class CryptoCurrency(models.Model):
    symbol = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    current_price = models.DecimalField(max_digits=25, decimal_places=4, blank=True, null=True)
    change_24h = models.DecimalField(max_digits=25, decimal_places=4, blank=True, null=True)
    trade_volume = models.DecimalField(max_digits=25, decimal_places=4, blank=True, null=True)
    vwap_24h = models.DecimalField(max_digits=25, decimal_places=4, blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.name


class UserFavorite(models.Model):
    crypto = models.ForeignKey(CryptoCurrency, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
