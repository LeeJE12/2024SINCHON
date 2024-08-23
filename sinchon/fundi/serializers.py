from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['eventName', 'startDate', 'endDate', 'budget', 'participants', 'club']
        read_only_fields = ['club']  # club 필드는 자동으로 설정되므로 읽기 전용으로 설정


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


