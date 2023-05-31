from django.contrib import admin
from cryptodata.models import CryptoCurrency, UserFavorite

admin.site.register(CryptoCurrency)
admin.site.register(UserFavorite)
