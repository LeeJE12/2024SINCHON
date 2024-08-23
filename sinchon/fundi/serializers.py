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

'''
class RegisterMemberSerializer(serializers.Serializer):
    event_id = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all())
    member_ids = serializers.ListField(
        child=serializers.PrimaryKeyRelatedField(queryset=Member.objects.all()),
        allow_empty=False
    )

    def create(self, validated_data):
        event = validated_data['event_id']
        member_ids = validated_data['member_ids']
        members = Member.objects.filter(id__in=member_ids)  # 주어진 ID의 멤버들 가져오기

        # 멤버들을 이벤트 참가자 목록에 추가
        for member in members:
            event.participants.add(member)

        event.save()
        return event
'''
class RegisterMemberSerializer(serializers.Serializer):
    member_ids = serializers.ListField(
        child=serializers.PrimaryKeyRelatedField(queryset=Member.objects.all()),
        allow_empty=False
    )

    def validate_member_ids(self, value):
        if not value:
            raise serializers.ValidationError("멤버 리스트가 비었습니다.")
        return value

class MoneyListSerializer(serializers.ModelSerializer):
    listid = serializers.IntegerField(source='id', read_only=True)
    total = serializers.IntegerField(source='budget', read_only=True)

    class Meta:
        model = MoneyList
        fields = ['listid', 'list', 'money', 'category', 'expense', 'receipt', 'eventid', 'date', 'total']
