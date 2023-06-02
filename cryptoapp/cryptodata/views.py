from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from rest_framework import viewsets

from .api import get_crypto_data, format_crypto_data, get_crypto_news
from .logic import filter_data
from .models import CryptoCurrency, UserFavorite
from .forms import RegistrationForm
from .serializers import CryptoCurrencySerializer


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


def news_list(request):
    news = get_crypto_news()

    context = {
        'news': news
    }
    return render(request, 'cryptodata/news_list.html', context)


@login_required
def crypto_list(request):
    api_data = get_crypto_data()
    formatted_data = format_crypto_data(api_data)

    search_query = request.GET.get('q')
    if search_query:
        filtered_data = filter_data(formatted_data, search_query)
    else:
        filtered_data = formatted_data

    for item in filtered_data:
        symbol = item['symbol']
        crypto, created = CryptoCurrency.objects.get_or_create(symbol=symbol)
        crypto.name = item['name']
        crypto.current_price = item['current_price']
        crypto.change_24h = item['change_24h']
        crypto.trade_volume = item['trade_volume']
        crypto.vwap_24h = item['vwap_24h']
        crypto.save()

    user_favorite = UserFavorite.objects.filter(user=request.user).values_list('crypto__name', flat=True)

    if filtered_data == formatted_data:
        user_favorites = UserFavorite.objects.filter(user=request.user)
        favorite_currencies = [favorite.crypto for favorite in user_favorites]
        other_currencies = CryptoCurrency.objects.exclude(pk__in=[currency.pk for currency in favorite_currencies])
        cryptocurrencies = list(favorite_currencies) + list(other_currencies)
    else:
        user_favorites = UserFavorite.objects.filter(user=request.user)
        favorite_currencies = [favorite.crypto for favorite in user_favorites]
        favorite_search_results = CryptoCurrency.objects.filter(
            Q(name__icontains=search_query) | Q(symbol__icontains=search_query),
            pk__in=[crypto.pk for crypto in favorite_currencies]
        )
        other_search_results = CryptoCurrency.objects.filter(
            Q(name__icontains=search_query) | Q(symbol__icontains=search_query)
        ).exclude(pk__in=[crypto.pk for crypto in favorite_currencies])
        cryptocurrencies = list(favorite_search_results) + list(other_search_results)

    if request.method == 'POST':
        crypto_symbol = request.POST.get('crypto_symbol')
        crypto = CryptoCurrency.objects.get(symbol=crypto_symbol)
        is_favorite = crypto.name in user_favorite
        if is_favorite:
            UserFavorite.objects.filter(user=request.user, crypto=crypto).delete()
        else:
            UserFavorite.objects.create(user=request.user, crypto=crypto)
        return redirect('crypto_list')

    context = {
        'cryptocurrencies': cryptocurrencies,
        'search_query': search_query,
        'favorite_currencies': user_favorite,
    }
    return render(request, 'cryptodata/crypto_list.html', context)


class CryptoCurrencyViewSet(viewsets.ModelViewSet):
    queryset = CryptoCurrency.objects.all()
    serializer_class = CryptoCurrencySerializer
    lookup_field = 'symbol'

