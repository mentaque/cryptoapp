import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cryptoapp.settings")
django.setup()

from rest_framework import status
from rest_framework.test import APITestCase
from .models import CryptoCurrency

class CryptoCurrencyAPITests(APITestCase):
    def setUp(self):
        self.crypto1 = CryptoCurrency.objects.create(symbol='BTC', name='Bitcoin')
        self.crypto2 = CryptoCurrency.objects.create(symbol='ETH', name='Ethereum')

    def test_get_all_cryptocurrencies(self):
        url = '/cryptocurrencies/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_crypto_currency(self):
        url = '/cryptocurrencies/BTC/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Bitcoin')

    def test_create_crypto_currency(self):
        url = '/cryptocurrencies/'
        data = {'symbol': 'LTC', 'name': 'Litecoin'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CryptoCurrency.objects.count(), 3)

    def test_update_crypto_currency(self):
        url = '/cryptocurrencies/ETH/'
        data = {'symbol': 'ETH', 'name': 'Ether'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Ether')
        self.crypto2.refresh_from_db()
        self.assertEqual(self.crypto2.name, 'Ether')

    def test_delete_crypto_currency(self):
        url = '/cryptocurrencies/BTC/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(CryptoCurrency.objects.filter(symbol='BTC').exists())
        self.assertEqual(CryptoCurrency.objects.count(), 1)

    def test_update_crypto_currency_invalid_data(self):
        url = '/cryptocurrencies/ETH/'
        data = {'symbol': 'ETH', 'name': ''}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_nonexistent_crypto_currency(self):
        url = '/cryptocurrencies/XYZ/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_nonexistent_crypto_currency(self):
        url = '/cryptocurrencies/XYZ/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(CryptoCurrency.objects.count(), 2)
