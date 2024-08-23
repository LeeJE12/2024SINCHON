from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *
from api.serializers import UserSerializer

class ClubSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Club
        fields = ['classname', 'classpw']
        read_only_fiels = ['user']

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['eventName', 'startDate', 'endDate', 'budget', 'participants', 'club']
        read_only_fields = ['club']  # club 필드는 자동으로 설정되므로 읽기 전용으로 설정

class MoneyListSerializer(serializers.ModelSerializer):
    listid = serializers.IntegerField(source='id', read_only=True)

    class Meta:
        model = MoneyList
        fields = ['listid', 'list', 'money', 'category', 'expense', 'receipt', 'eventid', 'date']