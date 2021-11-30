from django.urls import path
from .views import *

app_name = 'product'
urlpatterns = [
    path('milg', product_milg, name='product-milg'),
]
