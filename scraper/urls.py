from django.urls import path
from .views import compare_prices
from scraper.views import *

urlpatterns = [
    path('', welcome, name='welcome'),
    path('search', compare_prices, name='index'),
    path('result/', Result, name='result'),
]
