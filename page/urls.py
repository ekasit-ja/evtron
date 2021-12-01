from django.urls import path
from .views import *

app_name = 'page'
urlpatterns = [
    path('', page_home, name='page-home'),
    path('about/', page_about, name='page-about'),
    path('contact/', page_contact, name='page-contact'),
    # path('career/', page_career, name='page-career'),
]
