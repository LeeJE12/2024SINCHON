from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

app_name = 'fundi'

urlpatterns = [
    path('newclub/', ClubCreateView.as_view(), name='clubcreate'),
    path('registerEvent/', EventCreateView.as_view(), name='registerEvent'),
    path('registerMember/<int:eventid>/', RegisterMemberView.as_view(), name='register-member'),
    path('moneylist/<int:eventid>/', MoneyListView.as_view(), name='moneylist'),
    path('moneylistcreate/expense/<int:eventid>/', MoneyListCreateExpenseView.as_view(), name='Expensemoney'),
    path('moneylistcreate/earn/<int:eventid>/', MoneyListCreateEarnView.as_view(), name='Earnmoney'),
    path('dashboard/<int:eventid>/', DashboardView.as_view(), name='dashboard'),
]
