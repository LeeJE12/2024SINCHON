from django.urls import path
# from .views import
from django.conf import settings
from django.conf.urls.static import static
from .views import *

app_name = 'fundi'

urlpatterns = [
    path('registerEvent/', EventCreateView.as_view(), name='registerEvent'),
]
