import random

# 사용자 기본 대사량(BMR) 계산
def calculate_bmr(user_data):
    if user_data['gender'] == 'male':
        return 10 * user_data['weight'] + 6.25 * user_data['height'] - 5 * user_data['age'] + 5
    else:
        return 10 * user_data['weight'] + 6.25 * user_data['height'] - 5 * user_data['age'] - 161

def calculate_tdee(bmr, user_activity_data):
    activity_multiplier = calculate_activity_multiplier(
        user_activity_data['lifestyle'],
        user_activity_data['exercise'],
        user_activity_data['sleep_category']
    )
    return round(bmr * activity_multiplier, 1)

# 추가 유틸리티 함수: get_job_factor, get_sleep_factor, get_exercise_factor
# 이 함수들은 알고리즘에서 직접 사용됩니다.

def adjust_macros(tdee, goal):
    if goal == 'lose_weight':
        return {'carbs': 0.5 * tdee, 'protein': 0.3 * tdee, 'fats': 0.2 * tdee}
    elif goal == 'gain_weight':
        return {'carbs': 0.6 * tdee, 'protein': 0.25 * tdee, 'fats': 0.15 * tdee}
    else:
        return {'carbs': 0.6 * tdee, 'protein': 0.2 * tdee, 'fats': 0.2 * tdee}

def generate_daily_meals(user_data, carbs_list, protein_list, fat_list):
    bmr = calculate_bmr(user_data)
    tdee = calculate_tdee(bmr, user_data)
    daily_macros = adjust_macros(tdee, user_data['goal'])
    meals = []
    for meal_time in user_data['meal_times']:
        meals.append({
            'meal_time': meal_time,
            'meal': generate_meal(carbs_list, protein_list, fat_list, daily_macros)
        })
    return meals

def generate_meal(carbs_list, protein_list, fat_list, macro_goals):
    return {
        'carbs': select_component(carbs_list, macro_goals['carbs']),
        'protein': select_component(protein_list, macro_goals['protein']),
        'fats': select_component(fat_list, macro_goals['fats'])
    }

def select_component(source_list, macro_goal):
    selected = []
    while not meets_macro_goal(selected, macro_goal):
        component = random.choice(source_list)
        selected.append(component)
    return selected

def meets_macro_goal(selected, macro_goal, tolerance=0.1):
    total_macro = sum(item['carbs'] for item in selected)
    lower_bound = macro_goal * (1 - tolerance)
    upper_bound = macro_goal * (1 + tolerance)
    return lower_bound <= total_macro <= upper_bound

def calculate_activity_multiplier(lifestyle, exercise_data, sleep_category):
    # 직업 활동 계수 직접 처리
    job_factors = {
        'active_job': 1.725,     
        'desk_job': 1.2,         
        'standing_job': 1.4,     
        'kitchen_job': 1.5,      
        'not_working': 1.2       
    }
    base_multiplier = job_factors.get(lifestyle, 1.2)

    # 수면 계수 직접 처리
    sleep_factors = {
        'under_4': 0.9,
        '5_6': 0.95,
        '7_8': 1.0,
        'over_9': 0.975
    }
    sleep_factor = sleep_factors.get(sleep_category, 1.0)

    # 운동 계산 직접 처리
    exercise_multiplier = 0
    if exercise_data['frequency']:
        exercise_intensity_factors = {
            'light': 0.1,
            'moderate': 0.2,
            'somewhat_intense': 0.3,
            'intense': 0.4
        }
        intensity_factor = exercise_intensity_factors.get(exercise_data['intensity'], 0.1)
        duration_factor = exercise_data['duration'] / 60.0
        exercise_multiplier = intensity_factor * duration_factor

    total_multiplier = base_multiplier + exercise_multiplier
    total_multiplier *= sleep_factor
    return total_multiplier