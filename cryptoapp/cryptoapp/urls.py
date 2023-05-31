from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include
from rest_framework import routers
from cryptodata.views import crypto_list, news_list, register, CryptoCurrencyViewSet
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register(r'cryptocurrencies', CryptoCurrencyViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('crypto/', crypto_list, name='crypto_list'),
    path('', news_list, name='news_list'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', register, name='register'),
    path('', include(router.urls)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
