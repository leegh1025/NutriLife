from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import GoalForm, MealChoiceForm, BasicInfoForm, AdditionalInfoForm, SleepDurationForm, LifestyleForm, ExerciseInfoForm, ExerciseIntensityForm, ExerciseTimeForm
from .models import UserInfo

def user_info_goal(request):
    if request.method == "POST":
        form = GoalForm(request.POST)
        if form.is_valid():
            # 선택된 목표를 세션에 저장
            request.session['goal'] = form.cleaned_data['goal']
            return redirect('/user_info/count/')
    else:
        form = GoalForm()
    
    return render(request, 'User/user_info_goal.html', {'form': form})


def user_info_count(request):
    if request.method == "POST":
        form = MealChoiceForm(request.POST)
        if form.is_valid():
            request.session['meal_choices'] = form.cleaned_data['meal_choices']
            return redirect('/user_info/basic/')
    else:
        form = MealChoiceForm()
    
    return render(request, 'User/user_info_count.html', {'form': form})


def user_info_basic(request):
    if request.method == "POST":
        form = BasicInfoForm(request.POST)
        if form.is_valid():
            request.session['birth_year'] = form.cleaned_data['birth_year']
            request.session['gender'] = form.cleaned_data['gender']
            return redirect('/user_info/additional')
    else:
        form = BasicInfoForm()
    
    return render(request, 'User/user_info_basic.html', {'form': form})



def user_info_additional(request):
    if request.method == "POST":
        form = AdditionalInfoForm(request.POST)
        if form.is_valid():
            height = form.cleaned_data['height']
            weight = form.cleaned_data['weight']
            target_weight = form.cleaned_data['target_weight']
            muscle = form.cleaned_data.get('muscle')
            body_fat_percent = form.cleaned_data.get('body_fat_percent')

            # 세션에 저장된 기존 데이터를 불러옴 (필요 시)
            goal = request.session.get('goal')
            meal_choices = request.session.get('meal_choices')
            birth_year = request.session.get('birth_year')
            gender = request.session.get('gender')

            # 모든 데이터를 UserInfo 모델에 저장
            user_info = UserInfo.objects.create(
                goal=goal,
                meal_choices=" ".join(meal_choices),  # 공백으로 구분하여 저장
                birth_year=birth_year,
                gender=gender,
                height=height,
                weight=weight,
                target_weight=target_weight,
                muscle=muscle,
                body_fat_percent=body_fat_percent,
            )
            user_info.save()

            return redirect('/user_info/sleep_duration')
    else:
        form = AdditionalInfoForm()

    return render(request, 'User/user_info_additional.html', {'form': form})


def user_info_sleep_duration(request):
    if request.method == "POST":
        form = SleepDurationForm(request.POST)
        if form.is_valid():
            request.session['sleep_duration'] = form.cleaned_data['sleep_duration']
            return redirect('/user_info/lifestyle')
    else:
        form = SleepDurationForm()
    
    return render(request, 'User/user_info_sleep_duration.html', {'form': form})

def user_info_lifestyle(request):
    if request.method == "POST":
        form = LifestyleForm(request.POST)
        if form.is_valid():
            request.session['lifestyle'] = form.cleaned_data['lifestyle']
            return redirect('/user_info/exercise')
    else:
        form = LifestyleForm()
    
    return render(request, 'User/user_info_lifestyle.html', {'form': form})

def user_info_exercise(request):
    if request.method == "POST":
        form = ExerciseInfoForm(request.POST)
        if form.is_valid():
            exercise_regular = form.cleaned_data['exercise_regular']
            request.session['exercise_regular'] = exercise_regular
            if exercise_regular == "yes":
                # "예"를 선택했을 경우, 운동 강도 페이지로 이동
                return redirect('/user_info/exercise_intensity/')
            else:
                # "아니요"를 선택했을 경우, 프로세스 종료
                return JsonResponse({"message": "운동 정보가 성공적으로 저장되었습니다. 프로세스가 종료됩니다."})
    else:
        form = ExerciseInfoForm()
    
    return render(request, 'User/user_info_exercise.html', {'form': form})

def user_info_exercise_intensity(request):
    # 사용자가 이전에 '예'를 선택했는지 확인
    if request.session.get('exercise_regular') != 'yes':
        # '예'를 선택하지 않았으면 이전 페이지로 리다이렉트
        return redirect('')
    
    if request.method == "POST":
        form = ExerciseIntensityForm(request.POST)
        if form.is_valid():
            # 선택된 운동 강도를 세션에 저장
            request.session['exercise_intensity'] = form.cleaned_data['intensity']
            return redirect('/user_info/exercise_time/')
    else:
        form = ExerciseIntensityForm()
    
    return render(request, 'User/user_info_exercise_intensity.html', {'form': form})

def user_info_exercise_time(request):
    if request.method == "POST":
        form = ExerciseTimeForm(request.POST)
        if form.is_valid():
            # 선택된 운동 시간을 세션에 저장
            request.session['exercise_time'] = form.cleaned_data['time']
            return JsonResponse({"message": "운동 시간이 성공적으로 저장되었습니다."})
    else:
        form = ExerciseTimeForm()
    
    return render(request, 'User/user_info_exercise_time.html', {'form': form})