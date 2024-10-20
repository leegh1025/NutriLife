from django import forms

class GoalForm(forms.Form):
    GOAL_CHOICES = [
        ("lose_weight", "뚜렷한 체중 감량 ↓"),
        ("gain_weight", "뚜렷한 체중 증량 ↑"),
        ("maintain_weight_lose", "적당한 체중 감량 또는 유지"),
        ("maintain_weight_gain", "적당한 체중 증량 또는 유지"),
    ]

    goal = forms.ChoiceField(choices=GOAL_CHOICES, widget=forms.RadioSelect)


class MealChoiceForm(forms.Form):
    MEAL_CHOICES = [
        ("breakfast", "아침"),
        ("lunch", "점심"),
        ("dinner", "저녁"),
    ]

    meal_choices = forms.MultipleChoiceField(choices = MEAL_CHOICES, widget=forms.CheckboxSelectMultiple)


class BasicInfoForm(forms.Form):
    GENDER_CHOICES = [
        ('M', '남성'),
        ('F', '여성'),
    ]
    
    birth_year = forms.IntegerField(label="출생년도")
    gender = forms.ChoiceField(choices=GENDER_CHOICES)


class AdditionalInfoForm(forms.Form):
    height = forms.FloatField(label="키 (cm)")
    weight = forms.FloatField(label="현재 체중 (kg)")
    target_weight = forms.FloatField(label="목표 체중 (kg)")
    muscle = forms.FloatField(label="골격근량 (kg)", required=False)
    body_fat_percent = forms.FloatField(label="체지방률 (%)", required=False)
