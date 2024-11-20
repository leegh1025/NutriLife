from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    goal = models.CharField(max_length=20) # 목표
    meal_choices = models.CharField(max_length = 50) # 추천받고 싶은 끼니 선택(아,점,저), 중복 가능
    birth_year = models.IntegerField()
    gender = models.CharField(max_length=1)
    height = models.FloatField()  # 키 (cm)
    weight = models.FloatField()  # 현재 체중 (kg)
    target_weight = models.FloatField()
    muscle = models.FloatField(null=True, blank=True)
    body_fat_percent = models.FloatField(null=True, blank=True)
    sleep_duration = models.CharField(max_length=10)
    lifestyle = models.CharField(max_length=15, null=True, blank=True)
    exercise_regular = models.CharField(max_length=3, null=True, blank=True)
    intensity = models.CharField(max_length=20, null=True, blank=True)
    time = models.CharField(max_length=15, null=True, blank=True)

