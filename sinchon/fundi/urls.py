from django.urls import path
# from .views import
from django.conf import settings
from django.conf.urls.static import static
from .views import *

app_name = 'fundi'

urlpatterns = [
    path('event/register/', EventCreateView.as_view(), name='event-register'),
    path('event/<int:event_id>/moneylist/',
         MoneyListView.as_view(), name='moneylist'),
]
