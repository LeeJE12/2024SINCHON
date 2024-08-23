from django.urls import path
from .views import SignupView, LoginView
from django.conf import settings
from django.conf.urls.static import static

app_name = 'api'

urlpatterns=[
    path('signup/', SignupView.as_view()),
    path('login/', LoginView.as_view()),
]