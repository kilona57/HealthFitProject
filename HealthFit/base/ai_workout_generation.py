import os
import django
# import sys
# sys.path.append('C:\\Users\\khrom\\Documents\\HealthFit')
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HealthFit/healthfit.settings')
# django.setup()
import os
import sys
import django

# Add the project root directory to the Python path
sys.path.append('C:\\Users\\khrom\\Documents\\HealthFit\\HealthFit')

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healthfit.settings')

# Initialize Django
django.setup()
import google.generativeai as genai

import json
from base.models import Exercise, Workout, UserProfile, WorkoutExercise
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
import datetime




GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key='AIzaSyA56tUTFKLGnE0RGla75u5Twc1Tvl-njWk')
model = genai.GenerativeModel('gemini-pro')


# genai.configure(api_key='AIzaSyA56tUTFKLGnE0RGla75u5Twc1Tvl-njWk')
# model = genai.GenerativeModel('gemini-pro')


@login_required
def generate_workout(request):
    if request.method == 'POST':
        selected_equipments = request.POST.getlist('equipments')
        selected_muscle = request.POST.get('muscle')
        print(selected_equipments, selected_muscle)
        print("Available equipment values:", list(Exercise.objects.values_list('equipment', flat=True).distinct()))
        print("Available muscle groups:", list(Exercise.objects.values_list('muscle_group', flat=True).distinct()))
        for selected_equipment in selected_equipments:
            print(selected_equipment)
            available_exercises = Exercise.objects.filter(
                equipment=selected_equipment,
                muscle_group=selected_muscle
            )
            print(available_exercises)
            if available_exercises:
                user_profile = UserProfile.objects.get(user=request.user)

                exercises_data = [
                    {
                        'name': ex.name,
                        'muscle_group': ex.muscle_group,
                        'difficulty': ex.difficulty,
                        'equipment': ex.equipment,
                        'calories': ex.calories
                    }
                    for ex in available_exercises
                ]

                prompt = f"""
                Ты - профессиональный фитнес-тренер API, который генерирует планы тренировок.
                Твой ответ должен быть только в формате JSON без дополнительного текста или пояснений.

                Параметры пользователя:
                - Цель тренировок: {user_profile.fitness_goal}
                - Уровень активности: {user_profile.activity}
                - Пол: {user_profile.sex}

                Доступные упражнения: {json.dumps(exercises_data, ensure_ascii=False)}

                Создай план тренировки по следующим правилам:
                1. Выбери 6-8 упражнений из списка доступных упражнений
                2. Используй только точные названия упражнений из предоставленного списка
                3. План должен соответствовать следующей структуре JSON:
                {{
                    "workout_name": "Название тренировки на русском, отражающее цель и группу прорабатываемых мышц",
                    "workout_description": "Краткое описание тренировки на русском",
                    "exercises": [
                        {{
                            "name": "Точное название упражнения из списка",
                            "sets": число от 2 до 5,
                            "reps": число от 10 до 60,
                            "rest_time_seconds": число от 10 до 30,
                            "order": порядковый номер, начиная с 1
                        }}
                    ]
                }}

                Ответ должен быть только в формате JSON. Не добавляй никакого дополнительного текста или пояснений.
                Все текстовые поля должны быть на русском языке.
                """

                try:
                    # Получаем ответ от модели
                    response = model.generate_content(prompt)

                    # Очищаем ответ от возможных маркеров кода и лишних символов
                    cleaned_response = response.text.strip()
                    if cleaned_response.startswith('```json'):
                        cleaned_response = cleaned_response[7:]
                    if cleaned_response.endswith('```'):
                        cleaned_response = cleaned_response[:-3]
                    cleaned_response = cleaned_response.strip()

                    # Для отладки
                    print("Raw response:", response.text)
                    print("Cleaned response:", cleaned_response)

                    workout_data = json.loads(cleaned_response)

                    # Фильтруем упражнения, оставляя только существующие в базе
                    existing_exercises = list(Exercise.objects.filter(
                        name__in=[ex['name'] for ex in workout_data['exercises']]
                    ).values_list('name', flat=True))

                    filtered_exercises = [
                        ex for ex in workout_data['exercises']
                        if ex['name'] in existing_exercises
                    ]

                    # Обновляем порядковые номера
                    for i, exercise in enumerate(filtered_exercises, 1):
                        exercise['order'] = i

                    # Обновляем список упражнений в данных тренировки
                    workout_data['exercises'] = filtered_exercises

                    # Создаем новую тренировку
                    workout = Workout.objects.create(
                        name=workout_data['workout_name'],
                        description=workout_data['workout_description'],
                        musle_group=selected_muscle,
                        equipment=selected_equipment,
                        difficulty_level=3,
                        created_by=request.user
                    )

                    # Создаем связи с упражнениями
                    for exercise_data in workout_data['exercises']:
                        exercise = Exercise.objects.get(name=exercise_data['name'], muscle_group=workout.musle_group,
                                                        equipment=workout.equipment)
                        WorkoutExercise.objects.create(
                            workout=workout,
                            exercise=exercise,
                            sets=exercise_data['sets'],
                            reps=exercise_data['reps'],
                            rest_time_seconds=exercise_data['rest_time_seconds'],
                            order=exercise_data['order'],
                            calories=round(exercise.calories * exercise_data['sets'] * exercise_data["reps"])
                        )

                except json.JSONDecodeError as e:
                    return render(request, 'workout_generated.html', {
                        'error': f"Ошибка в формате JSON: {str(e)}\nОтвет API: {response.text}",
                        'success': False
                    })
                except Exception as e:
                    return render(request, 'workout_generated.html', {
                        'error': f"Ошибка: {str(e)}\nОтвет API: {response.text}",
                        'success': False
                    })

        return JsonResponse({'status': 'success'})

#
# import json
# import os
# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render
# from django.http import JsonResponse
# from .models import Exercise, Workout, UserProfile, WorkoutExercise
# from .ai import initialize_generativeai, generate_workout_plan
#
# # Инициализация Google Generative AI
# GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
# initialize_generativeai(GOOGLE_API_KEY)
#
# @login_required
# def generate_workout(request):
#     if request.method == 'POST':
#         selected_equipments = request.POST.getlist('equipments')
#         selected_muscle = request.POST.get('muscle')
#         print(selected_equipments, selected_muscle)
#
#         for selected_equipment in selected_equipments:
#             available_exercises = Exercise.objects.filter(
#                 equipment=selected_equipment,
#                 muscle_group=selected_muscle
#             )
#
#             if available_exercises:
#                 user_profile = UserProfile.objects.get(user=request.user)
#
#                 exercises_data = [
#                     {
#                         'name': ex.name,
#                         'muscle_group': ex.muscle_group,
#                         'difficulty': ex.difficulty,
#                         'equipment': ex.equipment,
#                         'calories': ex.calories
#                     }
#                     for ex in available_exercises
#                 ]
#
#                 prompt = f"""
#                 Ты - профессиональный фитнес-тренер API, который генерирует планы тренировок.
#                 Твой ответ должен быть только в формате JSON без дополнительного текста или пояснений.
#
#                 Параметры пользователя:
#                 - Цель тренировок: {user_profile.fitness_goal}
#                 - Уровень активности: {user_profile.activity}
#                 - Пол: {user_profile.sex}
#
#                 Доступные упражнения: {json.dumps(exercises_data, ensure_ascii=False)}
#
#                 Создай план тренировки по следующим правилам:
#                 1. Выбери 6-8 упражнений из списка доступных упражнений
#                 2. Используй только точные названия упражнений из предоставленного списка
#                 3. План должен соответствовать следующей структуре JSON:
#                 {{
#                     "workout_name": "Название тренировки на русском, отражающее цель и группу прорабатываемых мышц",
#                     "workout_description": "Краткое описание тренировки на русском",
#                     "exercises": [
#                         {{
#                             "name": "Точное название упражнения из списка",
#                             "sets": число от 2 до 5,
#                             "reps": число от 10 до 60,
#                             "rest_time_seconds": число от 10 до 30,
#                             "order": порядковый номер, начиная с 1
#                         }}
#                     ]
#                 }}
#
#                 Ответ должен быть только в формате JSON. Не добавляй никакого дополнительного текста или пояснений.
#                 Все текстовые поля должны быть на русском языке.
#                 """
#
#                 try:
#                     workout_data = generate_workout_plan(prompt)
#
#                     # Фильтруем упражнения, оставляя только существующие в базе
#                     existing_exercises = list(Exercise.objects.filter(
#                         name__in=[ex['name'] for ex in workout_data['exercises']]
#                     ).values_list('name', flat=True))
#
#                     filtered_exercises = [
#                         ex for ex in workout_data['exercises']
#                         if ex['name'] in existing_exercises
#                     ]
#
#                     # Обновляем порядковые номера
#                     for i, exercise in enumerate(filtered_exercises, 1):
#                         exercise['order'] = i
#
#                     # Обновляем список упражнений в данных тренировки
#                     workout_data['exercises'] = filtered_exercises
#
#                     # Создаем новую тренировку
#                     workout = Workout.objects.create(
#                         name=workout_data['workout_name'],
#                         description=workout_data['workout_description'],
#                         musle_group=selected_muscle,
#                         equipment=selected_equipment,
#                         difficulty_level=3,
#                         created_by=request.user
#                     )
#
#                     # Создаем связи с упражнениями
#                     for exercise_data in workout_data['exercises']:
#                         exercise = Exercise.objects.get(name=exercise_data['name'], muscle_group=workout.musle_group,
#                                                         equipment=workout.equipment)
#                         WorkoutExercise.objects.create(
#                             workout=workout,
#                             exercise=exercise,
#                             sets=exercise_data['sets'],
#                             reps=exercise_data['reps'],
#                             rest_time_seconds=exercise_data['rest_time_seconds'],
#                             order=exercise_data['order'],
#                             calories=round(exercise.calories * exercise_data['sets'] * exercise_data["reps"])
#                         )
#
#                 except json.JSONDecodeError as e:
#                     return render(request, 'workout_generated.html', {
#                         'error': f"Ошибка в формате JSON: {str(e)}",
#                         'success': False
#                     })
#                 except Exception as e:
#                     return render(request, 'workout_generated.html', {
#                         'error': f"Ошибка: {str(e)}",
#                         'success': False
#                     })
#
#         return JsonResponse({'status': 'success'})