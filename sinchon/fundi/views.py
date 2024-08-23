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


'''
class EventCreateView(views.APIView):
    permission_classes = [IsAuthenticated]  # 로그인된 사용자만 접근 가능

    def post(self, request):
        user = request.user  # 현재 로그인된 사용자
        try:
            # 사용자의 동아리 찾기 (로그인한 클럽에 연결)
            #club = Club.objects.get(user=user)  # Club 모델이 User와 연결된 경우
            
            
            # 사용자의 첫 번째 클럽 선택
            club = Club.objects.filter(user=user).first()
            if not club:
                return Response({'message': '동아리가 존재하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)
            
            
        except Club.DoesNotExist:
            return Response({'message': '동아리가 존재하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        data = request.data.copy()
        data['club'] = club.id  # 현재 로그인한 사용자의 동아리 ID를 데이터에 추가

        serializer = EventSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': '행사 추가 성공', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'message': '행사 추가 실패', 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
'''


class EventCreateView(views.APIView):
    permission_classes = [IsAuthenticated]  # 로그인된 사용자만 접근 가능

    def post(self, request):
        user = request.user  # 현재 로그인된 사용자
        try:
            # 사용자의 동아리 찾기 (로그인한 클럽에 연결)
            club = Club.objects.filter(user=user).first()
            if not club:
                return Response({'message': '동아리가 존재하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        except Club.DoesNotExist:
            return Response({'message': '동아리가 존재하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        data = request.data.copy()
        serializer = EventSerializer(data=data)

        if serializer.is_valid():
            serializer.save(club=club)  # club 인스턴스를 명시적으로 전달
            return Response({'message': '행사 추가 성공', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'message': '행사 추가 실패', 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class RegisterMemberView(views.APIView):
    permission_classes = [IsAuthenticated]  # 인증된 사용자만 접근 가능

    def post(self, request, eventid):  # URL에서 eventid를 받아옴
        event = get_object_or_404(Event, id=eventid)  # 이벤트 조회
        club = event.club  # 이벤트가 속한 클럽 가져오기

        serializer = RegisterMemberSerializer(data=request.data)
        if serializer.is_valid():
            # 새로운 멤버 생성 (이벤트의 클럽 정보 사용)
            member_name = serializer.validated_data.get('member_name')
            member = Member.objects.create(membername=member_name, club=club)

            # 멤버를 이벤트 참가자 목록에 추가
            event.participants.add(member)
            event.save()

            return Response({'message': '해당 행사 참여 부원 등록 성공', 'member': member.membername}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MoneyListCreateExpenseView(views.APIView):
    def post(self, request, eventid):
        data = request.data.copy()
        data['eventid'] = eventid
        data['expense'] = True

        serializer = MoneyListSerializer(data=data)
        if serializer.is_valid():
            moneylist = serializer.save()

            event = moneylist.eventid
            event.budget -= moneylist.money
            event.save()

            moneylist.budget = event.budget
            moneylist.save()

            return Response({'message': '지출기록 추가 성공', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'message': '지출기록 추가 실패', 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class MoneyListCreateEarnView(views.APIView):
    def post(self, request, eventid):
        data = request.data.copy()
        data['eventid'] = eventid
        data['expense'] = False

        serializer = MoneyListSerializer(data=data)
        if serializer.is_valid():
            moneylist = serializer.save()

            event = moneylist.eventid
            event.budget += moneylist.money
            event.save()

            moneylist.budget = event.budget
            moneylist.save()

            return Response({'message': '수입기록 추가 성공', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'message': '수입기록 추가 실패', 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class MoneyListView(views.APIView):
    def get(self, request, eventid, *args, **kwargs):
        event = get_object_or_404(Event, id=eventid)
        club = event.club
        clubevent = Event.objects.filter(club=club).values('id', 'eventName')

        moneylists = MoneyList.objects.filter(eventid=eventid).order_by('-id')
        expense = request.query_params.get('expense')
        if expense is not None:
            moneylists = moneylists.filter(expense=expense).order_by('-id')

        serializer = MoneyListSerializer(moneylists, many=True)
        # serialized_data = serializer.data.copy()

        # for item in serialized_data:
        #    item.update({'total': event.budget})

        return Response({
            'message': 'MoneyList get 성공',
            'clubevents': list(clubevent),
            'data': serializer.data
        }, status=status.HTTP_200_OK)


class DashboardView(views.APIView):
    def get(self, request, eventid, *args, **kwargs):
        event = get_object_or_404(Event, id=eventid)
        club = event.club
        clubevent = Event.objects.filter(club=club).values('id', 'eventName')

        moneylists = MoneyList.objects.filter(eventid=eventid)

        topThree = moneylists.order_by('-id')[:3]
        expenseLists = moneylists.filter(expense=True)
        earnLists = moneylists.filter(expense=False)

        forSnack = moneylists.filter(category="간식비").count()
        forPromotion = moneylists.filter(category="홍보비").count()
        forSubsidy = moneylists.filter(category="활동지원금").count()
        forEtc = moneylists.filter(category="기타").count()

        total_count = moneylists.count()

        totalExpense = 0
        for item in expenseLists:
            totalExpense += item.money

        totalEarn = 0
        for item in earnLists:
            totalEarn += item.money

        money_data = {
            'total' : event.budget,
            'totalexpense' : totalExpense,
            'totalearn' : totalEarn,
        }

        serializer = MoneyListSerializer(topThree, many=True)
        dashboard_data = {
            'summary': '최근 거래 내역 (3개)',
            'top_moneylists': serializer.data
        }

        category_data = {
            'snack_percentage': (forSnack / total_count * 100) if total_count else 0,
            'promotion_percentage': (forPromotion / total_count * 100) if total_count else 0,
            'subsidy_percentage': (forSubsidy / total_count * 100) if total_count else 0,
            'etc_percentage': (forEtc / total_count * 100) if total_count else 0,
        }

        return Response({
            'message': 'Dashboard data created',
            'clubevents': list(clubevent), 
            'eventname' : event.eventName,
            'moneydata' : money_data,
            'categorydata' : category_data,
            'data': dashboard_data
            }, status=status.HTTP_201_CREATED)
