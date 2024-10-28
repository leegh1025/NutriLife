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

class SleepDurationForm(forms.Form):
    SLEEP_CHOICES = [
        ("under_4", "4시간 이하"),
        ("5_6", "5 ~ 6시간"),
        ("7_8", "7 ~ 8시간"),
        ("over_9", "9시간 이상")
    ]

    sleep_duration = forms.ChoiceField(label="하루 평균 수면 시간", choices=SLEEP_CHOICES, widget=forms.RadioSelect)

class LifestyleForm(forms.Form):
    LIFESTYLE_CHOICES = [
        ("active_job", "활동적인 일을 하고 있어요 (영업직, 운동선수, 트레이너 등)"),
        ("desk_job", "주로 앉아서 근무해요 (사무직, 학생 등)"),
        ("standing_job", "주로 서서 근무해요 (승무원, 교사 등)"),
        ("kitchen_job", "가정 및 주방 일을 하고 있어요 (요식업자, 주부 등)"),
        ("not_working", "현재는 쉬고 있어요 (휴직, 무직 등)"),
    ]

    lifestyle = forms.ChoiceField(label="주로 어떤 일을 하나요?", choices=LIFESTYLE_CHOICES, widget=forms.RadioSelect)


class ExerciseInfoForm(forms.Form):
    EXERCISE_CHOICES = [
        ("yes", "예"),
        ("no", "아니요"),
    ]

    exercise_regular = forms.ChoiceField(label="주 3회 이상 꾸준히 운동하나요?", choices=EXERCISE_CHOICES, widget=forms.RadioSelect)


class ExerciseIntensityForm(forms.Form):
    INTENSITY_CHOICES = [
        ("light", "가볍게 - 호흡이 자연스럽고 대화가 가능한"),
        ("moderate", "보통 - 숨이 약간 차고 대화가 가능한"),
        ("somewhat_intense", "조금 강하게 - 숨이 가빠지며 대화가 조금 어려운"),
        ("intense", "매우 강하게 - 숨이 매우 헐떡이며 대화가 불가능한")
    ]

    intensity = forms.ChoiceField(label="어떤 강도로 운동을 하나요?", choices=INTENSITY_CHOICES, widget=forms.RadioSelect)