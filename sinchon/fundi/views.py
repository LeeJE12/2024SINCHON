from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, views
from django.shortcuts import get_object_or_404
from .models import *
from .serializers import *


class ClubCreateView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ClubSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({'message': '동아리 생성 성공', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'messange': '동아리 생성 실패', 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class EventCreateView(views.APIView):
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


class MoneyListCreateView(views.APIView):
    def post(self, request, eventid):

        data = request.data.copy()
        data['eventid'] = eventid

        serializer = MoneyListSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': '행사 추가 성공', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'message': '행사 추가 실패', 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
