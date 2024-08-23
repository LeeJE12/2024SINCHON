from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *
from api.serializers import UserSerializer


class ClubSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Club
        fields = ['clubname', 'clubpw', 'user']
        read_only_fiels = ['user']


class EventSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(
        queryset=Member.objects.all(),
        many=True,
        required=False  # 필수가 아님을 명시
    )
    
    class Meta:
        model = Event
        fields = ['eventName', 'startDate', 'endDate',
                  'budget', 'participants', 'club']
        read_only_fields = ['club']  # club 필드는 자동으로 설정되므로 읽기 전용으로 설정

class RegisterMemberSerializer(serializers.Serializer):
    member_name = serializers.CharField(max_length=100)  # 부원의 이름을 받아오기 위한 필드

    def validate_member_name(self, value):
        if not value:
            raise serializers.ValidationError("멤버이름이 필요합니다.")
        return value
    '''
    def get_or_create_member(self, club):
        member_name = self.validated_data.get('member_name')
        member, created = Member.objects.get_or_create(membername=member_name, club=club)
        return member
    '''


class MoneyListSerializer(serializers.ModelSerializer):
    listid = serializers.IntegerField(source='id', read_only=True)
    total = serializers.IntegerField(source='budget', read_only=True)

    class Meta:
        model = MoneyList
        fields = ['listid', 'list', 'money', 'category',
                  'expense', 'receipt', 'eventid', 'date', 'total']
