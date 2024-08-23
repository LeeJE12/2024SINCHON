from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

app_name = 'fundi'

urlpatterns = [
    path('newclub/', ClubCreateView.as_view(), name='clubcreate'),
    path('registerEvent/', EventCreateView.as_view(), name='registerEvent'),
    path('moneylist/<int:eventid>/', MoneyListView.as_view(), name='moneylist'),
    path('moneylistcreate/<int:eventid>/', MoneyListCreateView.as_view(), name='moneylistcreate')
]
