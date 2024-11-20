from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import GoalForm, MealChoiceForm, BasicInfoForm, AdditionalInfoForm, SleepDurationForm, LifestyleForm, ExerciseInfoForm, ExerciseIntensityForm, ExerciseTimeForm
from .models import UserInfo
from .utils import calculate_bmr, calculate_tdee, adjust_macros, generate_daily_meals
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .utils import image_map  
from .utils import add_images_to_meals

class SignupView(CreateView):
    template_name = 'User/signup.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')

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
                request.session['exercise_intensity'] = "light"
                request.session['exercise_time'] = "under_30"
                save_user_info(request)  # 데이터 저장
                return redirect('user_info_complete')
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

@login_required
def user_info_complete(request):
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
        {'name': '쌀밥', 'carbs': 40, 'protein': 3, 'fat': 0.5, 'serving_size': 100},
        {'name': '고구마', 'carbs': 27, 'protein': 2, 'fat': 0.1, 'serving_size': 100},
        {'name': '통밀 파스타', 'carbs': 30, 'protein': 5, 'fat': 1.2, 'serving_size': 100},
        {'name': '빵', 'carbs': 25, 'protein': 6, 'fat': 1.5, 'serving_size': 50}, 
        {'name': '옥수수', 'carbs': 29, 'protein': 3, 'fat': 1.0, 'serving_size': 100},  
        {'name': '바나나', 'carbs': 27, 'protein': 1, 'fat': 0.3, 'serving_size': 100}
    ]
    protein_list = [
        {'name': '닭가슴살', 'carbs': 0, 'protein': 25, 'fat': 1.5, 'serving_size': 100},
        {'name': '계란', 'carbs': 1, 'protein': 6, 'fat': 5, 'serving_size': 50},
        {'name': '두부', 'carbs': 3, 'protein': 8, 'fat': 4, 'serving_size': 100},
        {'name': '연어', 'carbs': 0, 'protein': 20, 'fat': 10, 'serving_size': 100}, 
        {'name': '소고기', 'carbs': 0, 'protein': 26, 'fat': 9, 'serving_size': 100},   
    ]
    fat_list = [
        {'name': '아몬드', 'carbs': 6, 'protein': 6, 'fat': 14, 'serving_size': 28},
        {'name': '아보카도', 'carbs': 9, 'protein': 2, 'fat': 15, 'serving_size': 75},
        {'name': '땅콩버터', 'carbs': 6, 'protein': 8, 'fat': 16, 'serving_size': 32},
        {'name': '치즈', 'carbs': 1, 'protein': 6, 'fat': 9, 'serving_size': 30}
    ]

    ready_meal_list = [
    {'name': '케이준 치킨 샐러드', 'carbs': 15, 'protein': 25, 'fat': 10, 'serving_size': 150},
    {'name': '그릴드 치킨 랩', 'carbs': 30, 'protein': 20, 'fat': 15, 'serving_size': 200},
    {'name': '훈제 연어 샐러드', 'carbs': 10, 'protein': 30, 'fat': 12, 'serving_size': 180},
    {'name': '머쉬룸 크림 스프', 'carbs': 20, 'protein': 5, 'fat': 8, 'serving_size': 250},
    {'name': '소고기 스테이크', 'carbs': 0, 'protein': 50, 'fat': 20, 'serving_size': 200},
    {'name': '그릴드 닭가슴살 플레이트', 'carbs': 10, 'protein': 40, 'fat': 8, 'serving_size': 200},
    {'name': '생선구이와 구운 채소', 'carbs': 15, 'protein': 35, 'fat': 7, 'serving_size': 200},
    {'name': '고구마 치킨 볼', 'carbs': 35, 'protein': 25, 'fat': 5, 'serving_size': 250},
    {'name': '단백질 팬케이크', 'carbs': 25, 'protein': 20, 'fat': 6, 'serving_size': 150},
    {'name': '오트밀과 블루베리', 'carbs': 30, 'protein': 10, 'fat': 5, 'serving_size': 200},
    {'name': '구운 연어와 퀴노아', 'carbs': 20, 'protein': 35, 'fat': 12, 'serving_size': 200},
    {'name': '두부 스크램블과 아보카도 토스트', 'carbs': 25, 'protein': 15, 'fat': 10, 'serving_size': 200},
    {'name': '저지방 치즈 오믈렛', 'carbs': 5, 'protein': 20, 'fat': 8, 'serving_size': 150},
    {'name': '단호박 퓨레와 닭가슴살', 'carbs': 25, 'protein': 35, 'fat': 6, 'serving_size': 220},
    {'name': '칠리 치킨과 브로콜리', 'carbs': 20, 'protein': 30, 'fat': 8, 'serving_size': 200},
]

    # 식단 생성
    meals = generate_daily_meals(user_data, carbs_list, protein_list, fat_list, ready_meal_list, meal_ratios)

    request.session['bmr'] = bmr
    request.session['tdee'] = tdee
    request.session['daily_macros'] = daily_macros
    request.session['meals'] = meals

        # BMR 계산 확인



    request.session.modified = True

    return redirect('user_info_results')




@login_required
def save_user_info(request):
    print("Session Data at save_user_info:", request.session.items())
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
    intensity = request.session.get('exercise_intensity', 'light')
    duration = request.session.get('exercise_time', 'under_30')
    
    # UserInfo에 데이터 저장
    user_info = UserInfo.objects.create(
        user=request.user,
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
        intensity=intensity,
        time=duration,
    )

    print("Saved User Info:", user_info)
    # 세션 정리

    return redirect('user_info_results')

@login_required
def user_info_results(request):
    # BMR, TDEE, daily_macros, meals 데이터 가져오기
    bmr = request.session.get('bmr')
    tdee = request.session.get('tdee')
    daily_macros = request.session.get('daily_macros')
    meals = request.session.get('meals')

    meals_with_images = add_images_to_meals(meals, image_map)

    # print("Session Data at user_info_results:", request.session.items())
    
    # 데이터 렌더링
    return render(request, 'User/results.html', {
        'bmr': bmr,
        'tdee': tdee,
        'daily_macros': daily_macros,
        'meals': meals_with_images,
    })

def refresh_meals(request):
    if request.method == "POST":
        # 세션에서 사용자 데이터를 가져오기
        user_data = {
            'height': request.session.get('height'),
            'weight': request.session.get('weight'),
            'gender': 'male' if request.session.get('gender') == 'M' else 'female',
            'age': 2024 - request.session.get('birth_year'),
            'activity_level': request.session.get('lifestyle'),
            'exercise': {
                'frequency': request.session.get('exercise_regular') == 'yes',
                'intensity': request.session.get('exercise_intensity'),
                'duration': int(request.session.get('exercise_time', 'under_30').split('_')[-1])
                if request.session.get('exercise_time') else 0
            },
            'sleep_category': request.session.get('sleep_duration'),
            'goal': request.session.get('goal'),
            'meal_times': request.session.get('meal_choices')
        }

        meal_ratios = {
            'breakfast': 0.3,
            'lunch': 0.4,
            'dinner': 0.3
        }

        # 기존 리스트 활용
        carbs_list = [
        {'name': '쌀밥', 'carbs': 40, 'protein': 3, 'fat': 0.5, 'serving_size': 100},
        {'name': '고구마', 'carbs': 27, 'protein': 2, 'fat': 0.1, 'serving_size': 100},
        {'name': '통밀 파스타', 'carbs': 30, 'protein': 5, 'fat': 1.2, 'serving_size': 100},
        {'name': '빵', 'carbs': 25, 'protein': 6, 'fat': 1.5, 'serving_size': 50}, 
        {'name': '옥수수', 'carbs': 29, 'protein': 3, 'fat': 1.0, 'serving_size': 100},  
        {'name': '바나나', 'carbs': 27, 'protein': 1, 'fat': 0.3, 'serving_size': 100}
    ]
        protein_list = [
            {'name': '닭가슴살', 'carbs': 0, 'protein': 25, 'fat': 1.5, 'serving_size': 100},
            {'name': '계란', 'carbs': 1, 'protein': 6, 'fat': 5, 'serving_size': 50},
            {'name': '두부', 'carbs': 3, 'protein': 8, 'fat': 4, 'serving_size': 100},
            {'name': '연어', 'carbs': 0, 'protein': 20, 'fat': 10, 'serving_size': 100}, 
            {'name': '소고기', 'carbs': 0, 'protein': 26, 'fat': 9, 'serving_size': 100},   
    ]
        fat_list = [
            {'name': '아몬드', 'carbs': 6, 'protein': 6, 'fat': 14, 'serving_size': 28},
            {'name': '아보카도', 'carbs': 9, 'protein': 2, 'fat': 15, 'serving_size': 75},
            {'name': '땅콩버터', 'carbs': 6, 'protein': 8, 'fat': 16, 'serving_size': 32},
            {'name': '치즈', 'carbs': 1, 'protein': 6, 'fat': 9, 'serving_size': 30}
    ]

        ready_meal_list = [
        {'name': '케이준 치킨 샐러드', 'carbs': 15, 'protein': 25, 'fat': 10, 'serving_size': 150},
        {'name': '그릴드 치킨 랩', 'carbs': 30, 'protein': 20, 'fat': 15, 'serving_size': 200},
        {'name': '훈제 연어 샐러드', 'carbs': 10, 'protein': 30, 'fat': 12, 'serving_size': 180},
        {'name': '머쉬룸 크림 스프', 'carbs': 20, 'protein': 5, 'fat': 8, 'serving_size': 250},
        {'name': '소고기 스테이크', 'carbs': 0, 'protein': 50, 'fat': 20, 'serving_size': 200},
        {'name': '그릴드 닭가슴살 플레이트', 'carbs': 10, 'protein': 40, 'fat': 8, 'serving_size': 200},
        {'name': '생선구이와 구운 채소', 'carbs': 15, 'protein': 35, 'fat': 7, 'serving_size': 200},
        {'name': '고구마 치킨 볼', 'carbs': 35, 'protein': 25, 'fat': 5, 'serving_size': 250},
        {'name': '단백질 팬케이크', 'carbs': 25, 'protein': 20, 'fat': 6, 'serving_size': 150},
        {'name': '오트밀과 블루베리', 'carbs': 30, 'protein': 10, 'fat': 5, 'serving_size': 200},
        {'name': '구운 연어와 퀴노아', 'carbs': 20, 'protein': 35, 'fat': 12, 'serving_size': 200},
        {'name': '두부 스크램블과 아보카도 토스트', 'carbs': 25, 'protein': 15, 'fat': 10, 'serving_size': 200},
        {'name': '저지방 치즈 오믈렛', 'carbs': 5, 'protein': 20, 'fat': 8, 'serving_size': 150},
        {'name': '단호박 퓨레와 닭가슴살', 'carbs': 25, 'protein': 35, 'fat': 6, 'serving_size': 220},
        {'name': '칠리 치킨과 브로콜리', 'carbs': 20, 'protein': 30, 'fat': 8, 'serving_size': 200},
    ]

        
        meals = generate_daily_meals(
            user_data=user_data,
            carbs_list=carbs_list,
            protein_list=protein_list,
            fat_list=fat_list,
            ready_meal_list=ready_meal_list,
            meal_ratios=meal_ratios,
        )

        # 세션에 새 식단 저장
        request.session['meals'] = meals
        request.session.modified = True

        return JsonResponse({"success": True})  # 성공 응답
    return JsonResponse({"success": False, "error": "Invalid request"})