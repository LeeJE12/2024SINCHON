from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import *
from .serializers import *


class MoneyListView(APIView):
    def get(self, request, event_id):
        # 해당 event_id에 대한 이벤트 객체 가져오기
        event = get_object_or_404(Event, pk=event_id)

        # MoneyList에서 해당 이벤트에 대한 상위 3개 항목 가져오기
        top_moneylist = MoneyList.objects.filter(
            eventid=event).order_by('-money')[:3]

        # 데이터를 시리얼라이즈하여 반환
        serializer = MoneyListSerializer(top_moneylist, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, event_id):
        # 해당 event_id에 대한 이벤트 객체 가져오기
        event = get_object_or_404(Event, pk=event_id)

        # POST 요청으로 받은 데이터에 eventid 추가
        data = request.data.copy()
        data['eventid'] = event.id

        # 데이터 시리얼라이징 및 유효성 검사
        serializer = MoneyListSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventCreateView(APIView):
    permission_classes = [IsAuthenticated]  # 로그인된 사용자만 접근 가능

    def post(self, request):
        user = request.user  # 현재 로그인된 사용자
        try:
            # 사용자의 동아리 찾기 (로그인한 클럽에 연결)
            club = Club.objects.get(user=user)  # Club 모델이 User와 연결된 경우
        except Club.DoesNotExist:
            return Response({'message': '동아리가 존재하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        data = request.data.copy()
        data['club'] = club.id  # 현재 로그인한 사용자의 동아리 ID를 데이터에 추가

        serializer = EventSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': '행사 추가 성공', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'message': '행사 추가 실패', 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
