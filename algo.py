import random

# 사용자 기본 대사량(BMR) 계산
def calculate_bmr(user_data):
    if user_data['gender'] == 'male':
        return 10 * user_data['weight'] + 6.25 * user_data['height'] - 5 * user_data['age'] + 5
    else:
        return 10 * user_data['weight'] + 6.25 * user_data['height'] - 5 * user_data['age'] - 161

def get_job_factor(lifestyle):
    
    job_factors = {
        'active_job': 1.725,     
        'desk_job': 1.2,         
        'standing_job': 1.4,     
        'kitchen_job': 1.5,      
        'not_working': 1.2       
    }
    
    return job_factors.get(lifestyle, 1.2)  

def get_sleep_factor(sleep_category):

    sleep_factors = {
        'under_4': 0.9,    # 심각한 수면 부족: -10% 대사량
        '5_6': 0.95,       # 수면 부족: -5% 대사량
        '7_8': 1.0,        # 적정 수면: 기준 대사량
        'over_9': 0.975    # 과다 수면: -2.5% 대사량
    }
    
    return sleep_factors.get(sleep_category, 1.0)

def get_exercise_factor(intensity):
    
    exercise_intensity_factors = {
        'light': 0.1,              # 가벼운 운동 (걷기, 요가 등)
        'moderate': 0.2,           # 중간 강도 (조깅, 자전거 등)
        'somewhat_intense': 0.3,    # 고강도 (러닝, 웨이트트레이닝 등)
        'intense': 0.4             # 매우 높은 강도 (HIIT, 크로스핏 등)
    }
    
    return exercise_intensity_factors.get(intensity, 0.1)

def calculate_activity_multiplier(lifestyle, exercise_data, sleep_category):
    
    base_multiplier = get_job_factor(lifestyle)
    
    # 직업이 active_job인 경우 운동 효과를 감소시킴 (이미 높은 활동량 반영)
    exercise_reduction = 0.7 if lifestyle == 'active_job' else 1.0
    
    # 3회 이상 운동하는 경우 운동 강도와 시간 반영
    if exercise_data['frequency']:
        intensity_factor = get_exercise_factor(exercise_data['intensity'])
        duration_factor = exercise_data['duration'] / 60.0
        exercise_multiplier = intensity_factor * duration_factor * exercise_reduction
        base_multiplier += exercise_multiplier
    
    # 수면 영향 계산
    sleep_factor = get_sleep_factor(sleep_category)
    base_multiplier *= sleep_factor
    
    return base_multiplier

def calculate_tdee(bmr, user_activity_data):
    """
    향상된 TDEE 계산 함수
    
    Parameters:
    bmr (float): 기초대사량
    user_activity_data (dict): {
        'lifestyle': str,  # LIFESTYLE_CHOICES 중 하나
        'exercise': {
            'frequency': bool,  # True if 주 3회 이상
            'intensity': str,
            'duration': int     # 분 단위
        },
        'sleep_category': str   # SLEEP_CHOICES 중 하나
    }
    
    Returns:
    float: 계산된 TDEE 값
    """
    activity_multiplier = calculate_activity_multiplier(
        user_activity_data['lifestyle'],
        user_activity_data['exercise'],
        user_activity_data['sleep_category']
    )
    
    return round(bmr * activity_multiplier, 1)  # 소수점 첫째자리까지 반올림
# 식단 목표에 따른 매크로 비율 조정
def adjust_macros(tdee, goal):
    if goal == 'lose_weight':
        return {'carbs': 0.5 * tdee, 'protein': 0.3 * tdee, 'fats': 0.2 * tdee}  # 체중 감량 5:3:2
    elif goal == 'gain_weight':
        return {'carbs': 0.6 * tdee, 'protein': 0.25 * tdee, 'fats': 0.15 * tdee}  # 체중 증량 6:2.5:1.5
    else:
        return {'carbs': 0.6 * tdee, 'protein': 0.2 * tdee, 'fats': 0.2 * tdee}  # 유지

# 식단 생성 - 끼니별로 탄수화물, 단백질, 지방 구성
def generate_meal(carbs_list, protein_list, fat_list, macro_goals):
    meal = {
        'carbs': select_component(carbs_list, macro_goals['carbs']),
        'protein': select_component(protein_list, macro_goals['protein']),
        'fats': select_component(fat_list, macro_goals['fats'])
    }
    return meal

# 목표 매크로 달성 여부 확인
def select_component(source_list, macro_goal):
    selected = []
    while not meets_macro_goal(selected, macro_goal):
        component = random.choice(source_list)
        selected.append(component)
    return selected

# 전체 식단 생성 - 끼니에 따라 맞춤 식단 제공
def generate_daily_meals(user_data, carbs_list, protein_list, fat_list):
    # 기본 대사량(BMR) 계산
    bmr = calculate_bmr(user_data)
    
    # 총 일일 에너지 소비량(TDEE) 계산 (활동 수준, 운동 강도, 운동 시간 반영)
    tdee = calculate_tdee(
        bmr,
        user_data['activity_level'],
        user_data['exercise_intensity'],
        user_data['exercise_duration'],
        user_data['regular_exercise']
    )

    # 목표에 따라 조정된 매크로 비율 설정
    daily_macros = adjust_macros(tdee, user_data['goal'])
    
    meals = []
    for meal_time in user_data['meal_times']:  # 사용자가 선택한 끼니에 맞춰 식단 생성
        meals.append({
            'meal_time': meal_time,
            'meal': generate_meal(carbs_list, protein_list, fat_list, daily_macros)
        })
    
    return meals

def meets_macro_goal(selected, macro_goals, tolerance=0.1):
    for macro, goal in macro_goals.items():
        total_macro = sum(item[macro] for item in selected)
        lower_bound = goal * (1 - tolerance)
        upper_bound = goal * (1 + tolerance)

        # 하나라도 목표를 충족하지 못하면 False 반환
        if not (lower_bound <= total_macro <= upper_bound):
            return False
    return True

# 예시 데이터 및 함수 호출
user_data = {
    'height': 175,  # 키 (cm)
    'weight': 70,   # 체중 (kg)
    'gender': 'male',  # 성별
    'age': 25,  # 연령대
    'activity_level': 1.2,  # 기본 활동 수준 (주로 앉아서 근무)
    'exercise_intensity': 'medium',  # 운동 강도
    'exercise_duration': 1,  # 하루 평균 운동 시간 (시간)
    'regular_exercise': True,  # 주 3회 이상 꾸준히 운동
    'goal': 'lose_weight',  # 식단 목표 (체중 감량)
    'meal_times': ['breakfast', 'lunch', 'dinner'],  # 추천받고 싶은 끼니 선택
    'occupation': 'office',  # 직업 (활동량 반영)
    'sleep_hours': 6  # 평균 수면 시간
}

# 탄수화물, 단백질, 지방 목록 생성 (사용자 맞춤 추천 식단을 위한 데이터)
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

# 식단 생성 예시
daily_meals = generate_daily_meals(user_data, carbs_list, protein_list, fat_list)
for meal in daily_meals:
    print(f"{meal['meal_time']}: {meal['meal']}")