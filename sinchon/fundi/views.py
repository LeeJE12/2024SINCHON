from django.shortcuts import render, get_object_or_404
from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status, views
from django.shortcuts import get_object_or_404, render
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


class RegisterMemberView(views.APIView):
    permission_classes = [IsAuthenticated]  # 인증된 사용자만 접근 가능

    def post(self, request):
        serializer = RegisterMemberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Member successfully registered to the event.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class MoneyListCreateView(views.APIView):
    def post(self, request, eventid):
        
        data = request.data.copy()
        data['eventid'] = eventid

        serializer = MoneyListSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': '행사 추가 성공', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'message': '행사 추가 실패', 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class MoneyListView(views.APIView):
    def get(self, request, eventid, *args, **kwargs):
        event = get_object_or_404(Event, id=eventid)
        club = event.club
        clubevent = Event.objects.filter(club=club).values('id', 'eventName')

        moneylists = MoneyList.objects.filter(eventid=eventid)
        expense = request.query_params.get('expense')
        if expense is not None:
            moneylists = moneylists.filter(expense=expense)
        
        serializer = MoneyListSerializer(moneylists, many=True)

        return Response({
            'message': 'MoneyList get 성공',
            'clubevents': list(clubevent),
            'data': serializer.data
        }, status=status.HTTP_200_OK)

class DashboardView(views.APIView):
    def post(self, request, eventid, *args, **kwargs):
        # 특정 eventid에 해당하는 MoneyList 중 상위 3개 항목을 가져옴
        moneylists = MoneyList.objects.filter(eventid=eventid).order_by('-id')[:3]
        
        serializer = MoneyListSerializer(moneylists, many=True)
        
        # 대시보드에 대한 처리 로직 (여기서는 단순히 데이터 반환으로 예시)
        dashboard_data = {
            'top_moneylists': serializer.data,
            'summary': 'This is a summary of the latest transactions.'
            # 추가적인 대시보드 데이터를 여기서 생성
        }

        return Response({'message': 'Dashboard data created', 'data': dashboard_data}, status=status.HTTP_201_CREATED)
