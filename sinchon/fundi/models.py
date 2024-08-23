from django.db import models
from api.models import User 
# Create your models here.

class Club(models.Model):
    clubname = models.CharField(max_length=100, unique=True,null=False)
    clubpw = models.CharField(max_length=128,null=False)  # 비밀번호는 해시로 저장
    # members 필드 삭제 (일대다 관계로 수정)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='clubs')  # Club을 관리하는 사용자
    
    def __str__(self):
        return self.clubname

class Member(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='members')  # Club과 일대다 관계
    membername = models.CharField(max_length=100)
    memberdues = models.DecimalField(max_digits=10, decimal_places=2)  # 회비, 금액 관련 필드이므로 DecimalField 사용

    def __str__(self):
        return f"{self.membername} ({self.club.clubname})"


class Dues(models.Model):
    money = models.IntegerField(null=False)  # 회비 금액
    club = models.ForeignKey(Club, on_delete=models.CASCADE) #Club과 일대일 관계.

    def __str__(self):
        return f"{self.club.clubname} - {self.money}"