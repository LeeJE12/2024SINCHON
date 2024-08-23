from django.db import models
from api.models import User 
# Create your models here.

class Club(models.Model):
    clubname = models.CharField(max_length=100, unique=True, null=False)
    clubpw = models.CharField(max_length=128,null=False)  # 비밀번호는 해시로 저장
    # members 필드 삭제 (일대다 관계로 수정)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='clubs')  # Club을 관리하는 사용자
    
    def __str__(self):
        return self.clubname


class Member(models.Model):
    club = models.ForeignKey(
        Club, on_delete=models.CASCADE, related_name='members')  # Club과 일대다 관계
    membername = models.CharField(max_length=100)
    memberdues = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.membername} ({self.club.clubname})"


class Dues(models.Model):
    money = models.IntegerField(null=False)  # 회비 금액
    club = models.ForeignKey(Club, on_delete=models.CASCADE) #Club과 일대일 관계.

    def __str__(self):
        return f"{self.club.clubname} - {self.money}"
    
class Event(models.Model):
    club = models.ForeignKey(
        Club, on_delete=models.CASCADE, related_name='events', null=False)  # 동아리와 1:N 관계
    eventName = models.CharField(max_length=100)
    startDate = models.DateField()
    endDate = models.DateField()
    budget = models.IntegerField(default=0)  # 예산을 정수로 표현
    participants = models.ManyToManyField(
        Member, related_name='events')  # 동아리원과 다대다 관계

    def __str__(self):
        return f"{self.eventName} ({self.club.clubname})"

# 자식 모델들

class MembershipFeeEvent(Event):  # 회비 사용 행사
    money = models.IntegerField()  # 인당회비


class PartialFeeEvent(Event):  # 회비 일부 사용 행사
    money = models.IntegerField()  # 인당회비
    discount = models.IntegerField()  # 인당 할인액


class NoFeeEvent(Event):  # 회비 미사용 행사
    money = models.IntegerField()  # 인당회비


class MoneyList(models.Model):
    list = models.CharField(max_length=200, blank=True, null=True)
    money = models.IntegerField(blank=True, null=True)
    eventid = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='eventlist')
    category = models.CharField(max_length=200, blank=True, null=True)
    expense = models.BooleanField(default=True)
    receipt = models.ImageField(blank=True, null=True)
    date = models.DateField('date published', blank=True, null=True, auto_now_add=True)
    budget = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.eventid.eventName} ({self.list})"
