from django.db import models

# Create your models here.
class UserInfo(models.Model):
    goal = models.CharField(max_length=20) # 목표
    meal_choices = models.CharField(max_length = 50) # 추천받고 싶은 끼니 선택(아,점,저), 중복 가능
    birth_year = models.IntegerField()
    gender = models.CharField(max_length=1)
    height = models.FloatField()  # 키 (cm)
    weight = models.FloatField()  # 현재 체중 (kg)
    target_weight = models.FloatField()
    muscle = models.FloatField(null=True, blank=True)
    body_fat_percent = models.FloatField(null=True, blank=True)

