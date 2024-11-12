import random

# 사용자 기본 대사량(BMR) 계산
def calculate_bmr(user_data):
    if user_data['gender'] == 'male':
        return 10 * user_data['weight'] + 6.25 * user_data['height'] - 5 * user_data['age'] + 5
    else:
        return 10 * user_data['weight'] + 6.25 * user_data['height'] - 5 * user_data['age'] - 161

def calculate_tdee(bmr, user_activity_data):
    activity_multiplier = calculate_activity_multiplier(
        user_activity_data['activity_level'],
        user_activity_data['exercise'],
        user_activity_data['sleep_category']
    )
    return round(bmr * activity_multiplier, 1)


def adjust_macros(tdee, goal):
    if goal == 'lose_weight':
        return {'carbs': 0.5 * tdee, 'protein': 0.3 * tdee, 'fats': 0.2 * tdee}
    elif goal == 'gain_weight':
        return {'carbs': 0.6 * tdee, 'protein': 0.25 * tdee, 'fats': 0.15 * tdee}
    elif goal == 'maintain_weight_lose':
        return {'carbs': 0.55 * tdee, 'protein': 0.25 * tdee, 'fats': 0.2 * tdee}
    elif goal == 'maintain_weight_gain':
        return {'carbs': 0.6 * tdee, 'protein': 0.2 * tdee, 'fats': 0.2 * tdee}
    else:
        # 기본값 (목표가 설정되지 않은 경우)
        return {'carbs': 0.6 * tdee, 'protein': 0.2 * tdee, 'fats': 0.2 * tdee}

def generate_daily_meals(user_data, carbs_list, protein_list, fat_list, meal_ratios):
    bmr = calculate_bmr(user_data)
    tdee = calculate_tdee(bmr, user_data)
    daily_macros = adjust_macros(tdee, user_data['goal'])


    meals = []
    for meal_time in user_data['meal_times']:
        ratio = meal_ratios[meal_time]
        macro_goals_per_meal = {
            'carbs': daily_macros['carbs'] * ratio,
            'protein': daily_macros['protein'] * ratio,
            'fats': daily_macros['fats'] * ratio
        } 
        meals.append({
            'meal_time': meal_time,
            'meal': generate_meal(carbs_list, protein_list, fat_list, macro_goals_per_meal)
        })
    return meals

def generate_meal(carbs_list, protein_list, fat_list, macro_goals):
    return {
        'carbs': calculate_portions(
            select_component(carbs_list, macro_goals['carbs'], 'carbs'),
            macro_goals['carbs'], 'carbs'
        ),
        'protein': calculate_portions(
            select_component(protein_list, macro_goals['protein'], 'protein'),
            macro_goals['protein'], 'protein'
        ),
        'fats': calculate_portions(
            select_component(fat_list, macro_goals['fats'], 'fat'),
            macro_goals['fats'], 'fat'
        ),
    }
    
def calculate_portions(selected_items, macro_goal, macro_key):
    total_macro = sum(item[macro_key] for item in selected_items) 
    portioned_items = []
    for item in selected_items:
        ratio = macro_goal / total_macro if total_macro > 0 else 0
        adjusted_amount = round(ratio * item[macro_key], 1)  
        portioned_items.append({'name': item['name'], 'amount': adjusted_amount})
    return portioned_items

def select_component(source_list, macro_goal, macro_key):
    selected = []
    total_macro = 0  
    for item in source_list:
        if total_macro >= macro_goal:
            break  # 목표치를 초과하면 중단
        selected.append(item)
        total_macro += item[macro_key]  
    return selected

def meets_macro_goal(selected, macro_goal, tolerance=0.1):
    total_macro = sum(item['carbs'] for item in selected)
    lower_bound = macro_goal * (1 - tolerance)
    upper_bound = macro_goal * (1 + tolerance)
    return lower_bound <= total_macro <= upper_bound

def calculate_activity_multiplier(activity_level, exercise_regular, sleep_duration):
    job_factors = {
        'active_job': 1.5,     
        'desk_job': 1.1,         
        'standing_job': 1.25,     
        'kitchen_job': 1.35,      
        'not_working': 1.1       
    }
    base_multiplier = job_factors.get(activity_level, 1.1)

    sleep_factors = {
        'under_4': 0.9,
        '5_6': 0.95,
        '7_8': 1.0,
        'over_9': 0.975
    }
    sleep_factor = sleep_factors.get(sleep_duration, 1.0)

    exercise_multiplier = 0
    if exercise_regular['frequency']:
        exercise_intensity_factors = {
            'light': 0.1,
            'moderate': 0.2,
            'somewhat_intense': 0.3,
            'intense': 0.4
        }
        intensity_factor = exercise_intensity_factors.get(exercise_regular['intensity'], 0.1)
        duration_factor = exercise_regular['duration'] / 60.0
        exercise_multiplier = intensity_factor * duration_factor

    total_multiplier = base_multiplier + exercise_multiplier
    total_multiplier *= sleep_factor
    return total_multiplier