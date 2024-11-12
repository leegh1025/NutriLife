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

    import datetime
    current_year = datetime.datetime.now().year
    age = current_year - birth_year

    # 사용자 데이터 준비
    user_data = {
        'height': height,
        'weight': weight,
        'gender': 'male' if gender == 'M' else 'female',
        'age': age,
        'activity_level': lifestyle,
        'exercise': {
            'frequency': exercise_regular == 'yes',
            'intensity': intensity,
            'duration': int(time.split('_')[-1]) if time else 0
        },
        'sleep_category': sleep_duration,
        'goal': goal,
        'meal_times': meal_choices if isinstance(meal_choices, list) else meal_choices.split(" ") if meal_choices else ['breakfast', 'lunch', 'dinner']
    }

    # BMR 계산
    bmr = calculate_bmr(user_data)
    # TDEE 계산
    tdee = calculate_tdee(bmr, user_data)
    # 매크로 비율 계산
    daily_macros = adjust_macros(tdee, goal)

    meal_ratios = {
        'breakfast': 0.3,  # 30% 아침
        'lunch': 0.4,      # 40% 점심
        'dinner': 0.3      # 30% 저녁
    }


    carbs_list = [
        {'name': '쌀밥', 'carbs': 40, 'protein': 3, 'fat': 0.5},
        {'name': '고구마', 'carbs': 27, 'protein': 2, 'fat': 0.1},
        {'name': '통밀 파스타', 'carbs': 30, 'protein': 5, 'fat': 1.2},
    ]
    protein_list = [
        {'name': '닭가슴살', 'carbs': 0, 'protein': 25, 'fat': 1.5},
        {'name': '계란', 'carbs': 1, 'protein': 6, 'fat': 5},
        {'name': '두부', 'carbs': 3, 'protein': 8, 'fat': 4},
    ]
    fat_list = [
        {'name': '아몬드', 'carbs': 6, 'protein': 6, 'fat': 14},
        {'name': '아보카도', 'carbs': 9, 'protein': 2, 'fat': 15},
        {'name': '땅콩버터', 'carbs': 6, 'protein': 8, 'fat': 16},
    ]

    # 식단 생성
    meals = generate_daily_meals(user_data, carbs_list, protein_list, fat_list, meal_ratios)

    request.session['bmr'] = bmr
    request.session['tdee'] = tdee
    request.session['daily_macros'] = daily_macros
    request.session['meals'] = meals

    return redirect('user_info_results')





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

def user_info_results(request):
    # BMR, TDEE, daily_macros, meals 데이터 가져오기
    bmr = request.session.get('bmr')
    tdee = request.session.get('tdee')
    daily_macros = request.session.get('daily_macros')
    meals = request.session.get('meals')

    # 데이터 렌더링
    return render(request, 'User/results.html', {
        'bmr': bmr,
        'tdee': tdee,
        'daily_macros': daily_macros,
        'meals': meals
    })