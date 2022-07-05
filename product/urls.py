from django.urls import path
from .views import *

app_name = 'product'
urlpatterns = [
    path('wind', product_wind, name='product-wind'),
    path('move', product_move, name='product-move'),
    path('carry', product_carry, name='product-carry'),
    path('max', product_max, name='product-max'),
    path('flash', product_flash, name='product-flash'),
    path('hawk', product_hawk, name='product-hawk'),
]
