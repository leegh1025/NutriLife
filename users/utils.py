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

def generate_daily_meals(user_data, carbs_list, protein_list, fat_list, ready_meal_list, meal_ratios):
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
        max_meal_calories = tdee * ratio
        meals.append({
            'meal_time': meal_time,
            'meal': generate_meal(carbs_list, protein_list, fat_list, macro_goals_per_meal, ready_meal_list,max_meal_calories)
        })
    return meals

def generate_meal(carbs_list, protein_list, fat_list, macro_goals, ready_meal_list, max_meal_calories):
    ready_meal = random.choice(ready_meal_list)
    ready_meal_calories = (ready_meal['carbs'] * 4) + (ready_meal['protein'] * 4) + (ready_meal['fat'] * 9)

    ready_meal_macros = {
        'carbs': ready_meal.get('carbs', 0),
        'protein': ready_meal.get('protein', 0),
        'fats': ready_meal.get('fats', 0)
    }

    remaining_calories = max(max_meal_calories - ready_meal_calories, 0)
    remaining_macros = {
        'carbs': max(macro_goals['carbs'] - ready_meal_macros['carbs'], 0),
        'protein': max(macro_goals['protein'] - ready_meal_macros['protein'], 0),
        'fats': max(macro_goals['fats'] - ready_meal_macros['fats'], 0)
    }

    additional_carbs = calculate_portions(
        select_component(carbs_list, remaining_macros['carbs'], 'carbs', max_items=2),
        min(remaining_macros['carbs'], remaining_calories / 4),  # 남은 칼로리도 고려
        'carbs'
    )
    remaining_calories -= sum(item['carbs'] * 4 for item in additional_carbs)

    additional_protein = calculate_portions(
        select_component(protein_list, remaining_macros['protein'], 'protein', max_items=2),
        min(remaining_macros['protein'], remaining_calories / 4),  # 남은 칼로리도 고려
        'protein'
    )
    remaining_calories -= sum(item['protein'] * 4 for item in additional_protein)

    additional_fats = calculate_portions(
        select_component(fat_list, remaining_macros['fats'], 'fat', max_items=2),
        min(remaining_macros['fats'], remaining_calories / 9),  # 남은 칼로리도 고려
        'fat'
    )
    remaining_calories -= sum(item['fat'] * 9 for item in additional_fats)


    total_macros = {
        'carbs': ready_meal_macros['carbs'] + sum(item['carbs'] for item in additional_carbs),
        'protein': ready_meal_macros['protein'] + sum(item['protein'] for item in additional_protein),
        'fats': ready_meal_macros['fats'] + sum(item['fat'] for item in additional_fats)
    }

    total_calories = ready_meal_calories + (
        sum(item['carbs'] * 4 for item in additional_carbs) +
        sum(item['protein'] * 4 for item in additional_protein) +
        sum(item['fat'] * 9 for item in additional_fats)
    )
    # 결과 반환
    print("=== Final Debug Info ===")
    print(f"Total Macros: {total_macros}")
    print(f"Total Calories: {total_calories}")

    return {
        'ready_meal': {'name': ready_meal['name'], 'amount': ready_meal['serving_size']},
        'additional_carbs': additional_carbs,
        'additional_protein': additional_protein,
        'additional_fats': additional_fats,
        'total_macros': {
            'carbs': ready_meal_macros['carbs'] + sum(item['carbs'] for item in additional_carbs),
            'protein': ready_meal_macros['protein'] + sum(item['protein'] for item in additional_protein),
            'fats': ready_meal_macros['fats'] + sum(item['fat'] for item in additional_fats)
        },
        'total_calories': total_calories
    }
    
def calculate_portions(selected_items, macro_goal, macro_key, min_amount=5):
    portioned_items = []
    remaining_macro = macro_goal  # 목표 매크로 남은 양

    for item in selected_items:
        # 음식별 매크로 비율 계산
        item_macro = item[macro_key] / item['serving_size']

        # 음식별 섭취 가능량 계산 (남은 매크로를 기준으로)
        max_servings = remaining_macro / item[macro_key] if item[macro_key] > 0 else 0
        adjusted_amount = min(max_servings * item['serving_size'], item['serving_size'] * 1.5)  # 최대 1.5배 서빙 제한

        # 섭취량이 유효할 경우 추가
        if adjusted_amount >= min_amount:  # 최소량 조건 추가
            portioned_items.append({
                'name': item['name'],
                'amount': round(adjusted_amount, 1),
                macro_key: round(adjusted_amount * item_macro, 1)  # 매크로 키 추가
            })
            remaining_macro -= adjusted_amount * item_macro   # 남은 매크로 양 업데이트
        
        # 목표치 달성 시 중단
        if remaining_macro <= 0.1 * macro_goal:  # 목표의 10% 이하로 남으면 중단
            break

    return portioned_items
def select_component(source_list, macro_goal, macro_key, max_items=1):

    random.shuffle(source_list)
    selected = []
    total_macro = 0  

    for item in source_list:
        if len(selected) >= max_items:  # 최대 음식 개수 제한
            break
        if total_macro + item[macro_key] > macro_goal:  # 목표치를 초과하면 중단
            continue
        selected.append(item)
        total_macro += item[macro_key]

        if total_macro >= macro_goal:  # 목표치에 도달하면 루프 종료
            break
        
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
        duration_mapping = {
            "under_30": 0.5,  # 30분 이하 -> 0.5시간
            "30_to_60": 1.0,  # 30~60분 -> 1시간
            "60_to_90": 1.5,  # 60~90분 -> 1.5시간
            "90_to_120": 2.0, # 90~120분 -> 2시간
            "over_120": 2.5   # 120분 초과 -> 2.5시간
        }
        duration_factor = duration_mapping.get(exercise_regular.get('duration', 'under_30'), 0.5)
        exercise_multiplier = intensity_factor * duration_factor

    total_multiplier = base_multiplier + exercise_multiplier
    total_multiplier *= sleep_factor
    return total_multiplier




image_map = {
    '케이준 치킨 샐러드': 'images/cajun.jpeg',
    '그릴드 치킨 랩': 'images/chickenwrap.jpeg',
    '훈제 연어 샐러드': 'images/salmon.jpeg',
    '머쉬룸 크림 스프': 'images/mushroom.jpeg',
    '소고기 스테이크': 'images/steak.jpeg',
    '그릴드 닭가슴살 플레이트': 'images/chickenbreast.jpeg',
    '생선구이와 구운 채소': 'images/fish.jpeg',
    '고구마 치킨 볼': 'images/chickenball.jpeg',
    '단백질 팬케이크': 'images/pancake.jpeg',
    '오트밀과 블루베리': 'images/oatmeal.jpeg',
    '구운 연어와 퀴노아': 'images/grilledsalmon.jpeg',
    '두부 스크램블과 아보카도 토스트': 'images/tofuscramble.jpeg',
    '저지방 치즈 오믈렛': 'images/omelette.jpeg',
    '단호박 퓨레와 닭가슴살': 'images/pumpkinpuree.jpeg',
    '칠리 치킨과 브로콜리': 'images/chillychicken.jpeg',
    '고구마' : 'images/sweetpotato.png',
    '통밀 파스타' : 'images/pasta.png',
    '쌀밥' : 'images/rice.png',
    '옥수수' : 'images/corn.png',
    '바나나' : 'images/banana.png',
    '빵' : 'images/bread.png',
    '닭가슴살' : 'images/chick.png',
    '계란' : 'images/egg.png',
    '두부' : 'images/tofu.png',
    '치즈' : 'images/cheese.png',
    '땅콩버터' : 'images/peanutbutter.png',
    '아보카도' : 'images/avocado.png',
    '아몬드' : 'images/almond.png',

}

def add_images_to_meals(meals, image_map):
    for meal in meals:
        # ready_meal에 해당하는 이미지 추가
        ready_meal_name = meal['meal']['ready_meal']['name']
        if ready_meal_name in image_map:
            meal['meal']['ready_meal']['image'] = image_map[ready_meal_name]  # 이미지가 없는 경우 기본 이미지

        # 탄수화물 항목에 이미지 추가
        for carb in meal['meal']['additional_carbs']:
            if carb['name'] in image_map:
                carb['image'] = image_map[carb['name']]
        

        # 단백질 항목에 이미지 추가
        for protein in meal['meal']['additional_protein']:
            if protein['name'] in image_map:
                protein['image'] = image_map[protein['name']]
        

        # 지방 항목에 이미지 추가
        for fat in meal['meal']['additional_fats']:
            if fat['name'] in image_map:
                fat['image'] = image_map[fat['name']]
    return meals

