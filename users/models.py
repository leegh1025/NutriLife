from django.db import models

# Create your models here.
class UserInfo(models.Model):
    GOAL_CHOICES = [
        ("lose_weight", "뚜렷한 체중 감량 ↓"),
        ("gain_weight", "뚜렷한 체중 증량 ↑"),
        ("maintain_weight_lose", "적당한 체중 감량 또는 유지"),
        ("maintain_weight_gain", "적당한 체중 증량 또는 유지"),
    ]

    MEAL_CHOICES = [
        ("breakfast", "아침"),
        ("lunch", "점심"),
        ("dinner", "저녁"),
    ]

    GENDER_CHOICES = [
        ('M', '남성'),
        ('F', '여성'),
    ]

    goal = models.CharField(max_length = 20, choices=GOAL_CHOICES) # 목표
    meal_choices = models.CharField(max_length = 50) # 추천받고 싶은 끼니 선택(아,점,저), 중복 가능
    birth_year = models.IntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    height = models.FloatField()  # 키 (cm)
    weight = models.FloatField()  # 현재 체중 (kg)
    target_weight = models.FloatField()
    muscle = models.FloatField(null=True, blank=True)
    body_fat_percent = models.FloatField(null=True, blank=True)



    def save_meals(self, meals):
        self.meal_choices = " ".join(meals)  
        self.save()