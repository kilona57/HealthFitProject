from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Exercise, Workout, WorkoutExercise
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View


@login_required
def create_workout(request):
    if request.method == 'POST':
        name = request.POST.get('name-f18c')
        description = request.POST.get('phone-cbff')
        musle_group = request.POST.get('select-9bba')
        equipment = request.POST.get('select-b0fa')
        difficulty_level = request.POST.get('date-33f9')

        workout = Workout.objects.create(
            name=name,
            description=description,
            musle_group=musle_group,
            equipment=equipment,
            difficulty_level=difficulty_level,
            created_by=request.user
        )
        return JsonResponse({'workout_id': workout.id})

    exercises = Exercise.objects.all()
    return render(request, 'create_workout_new.html', {'exercises': exercises})


@login_required
def add_exercise_to_workout(request):
    if request.method == 'POST':
        workout_id = request.POST.get('workout_id')
        exercise_id = request.POST.get('exercise_id')
        sets = request.POST.get('sets')
        reps = request.POST.get('reps')
        rest_time = request.POST.get('rest_time')
        order = request.POST.get('order')

        workout = get_object_or_404(Workout, id=workout_id, created_by=request.user)
        exercise = get_object_or_404(Exercise, id=exercise_id)

        new_exercise_in_workout = WorkoutExercise.objects.create(
            workout=workout,
            exercise=exercise,
            sets=sets,
            reps=reps,
            rest_time_seconds=rest_time,
            order=order,
            calories=int(sets) * int(reps) * exercise.calories
        )
        return JsonResponse({'status': 'success'})
