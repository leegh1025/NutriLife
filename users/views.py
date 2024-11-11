from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import GoalForm, MealChoiceForm, BasicInfoForm, AdditionalInfoForm, SleepDurationForm, LifestyleForm, ExerciseInfoForm, ExerciseIntensityForm, ExerciseTimeForm
from .models import UserInfo
from .utils import calculate_bmr, calculate_tdee, adjust_macros, generate_daily_meals

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
            request.session['height'] = form.cleaned_data['height']
            request.session['weight'] = form.cleaned_data['weight']
            request.session['target_weight'] = form.cleaned_data['target_weight']
            request.session['muscle'] = form.cleaned_data.get('muscle')
            request.session['body_fat_percent'] = form.cleaned_data.get('body_fat_percent')

            # 세션에 저장된 기존 데이터를 불러옴 (필요 시)
            goal = request.session.get('goal')
            meal_choices = request.session.get('meal_choices')
            birth_year = request.session.get('birth_year')
            gender = request.session.get('gender')

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
                return save_user_info(request) 
    else:
        form = ExerciseInfoForm()
    
    return render(request, 'User/user_info_exercise.html', {'form': form})

def user_info_exercise_intensity(request):
    exercise_regular = request.session.get('exercise_regular')
    print("운동 여부 (강도 페이지):", exercise_regular)
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
            return redirect('/user_info/complete/')
    else:
        form = ExerciseTimeForm()
    
    return render(request, 'User/user_info_exercise_time.html', {'form': form})

def user_info_complete(request):
    print("user_info_complete 뷰가 호출되었습니다.")
    # 세션에서 모든 데이터 가져오기
    goal = request.session.get('goal')
    meal_choices = request.session.get('meal_choices')
    birth_year = request.session.get('birth_year')
    gender = request.session.get('gender')
    height = request.session.get('height')
    weight = request.session.get('weight')
    target_weight = request.session.get('target_weight')
    muscle = request.session.get('muscle')
    body_fat_percent = request.session.get('body_fat_percent')
    sleep_duration = request.session.get('sleep_duration')
    lifestyle = request.session.get('lifestyle')
    exercise_regular = request.session.get('exercise_regular')
    intensity = request.session.get('exercise_intensity')
    time = request.session.get('exercise_time')

    # 데이터베이스에 저장
    user_info = UserInfo.objects.create(
        goal=goal,
        meal_choices=" ".join(meal_choices) if meal_choices else None,  # 리스트일 경우 문자열로 변환
        birth_year=birth_year,
        gender=gender,
        height=height,
        weight=weight,
        target_weight=target_weight,
        muscle=muscle,
        body_fat_percent=body_fat_percent,
        sleep_duration=sleep_duration,
        lifestyle=lifestyle,
        exercise_regular=exercise_regular,
        intensity=intensity,
        time=time,
    )
    user_info.save()


    return JsonResponse({"message": "모든 정보가 성공적으로 저장되었습니다."})

def save_user_info(request):
    # 세션에서 필요한 데이터 가져오기
    goal = request.session.get('goal')
    meal_choices = request.session.get('meal_choices')
    birth_year = request.session.get('birth_year')
    gender = request.session.get('gender')
    height = request.session.get('height')
    weight = request.session.get('weight')
    target_weight = request.session.get('target_weight')
    muscle = request.session.get('muscle')
    body_fat_percent = request.session.get('body_fat_percent')
    sleep_duration = request.session.get('sleep_duration')
    lifestyle = request.session.get('lifestyle')
    exercise_regular = request.session.get('exercise_regular')
    
    # UserInfo에 데이터 저장
    user_info = UserInfo.objects.create(
        goal=goal,
        meal_choices=" ".join(meal_choices) if meal_choices else None,
        birth_year=birth_year,
        gender=gender,
        height=height,
        weight=weight,
        target_weight=target_weight,
        muscle=muscle,
        body_fat_percent=body_fat_percent,
        sleep_duration=sleep_duration,
        lifestyle=lifestyle,
        exercise_regular=exercise_regular,
    )

    request.session.flush()  # 세션 정리

    return JsonResponse({"message": "모든 정보가 성공적으로 저장되었습니다."})