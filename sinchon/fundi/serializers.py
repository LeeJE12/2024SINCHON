from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['eventName', 'startDate', 'endDate', 'budget', 'participants', 'club']
        read_only_fields = ['club']  # club 필드는 자동으로 설정되므로 읽기 전용으로 설정
