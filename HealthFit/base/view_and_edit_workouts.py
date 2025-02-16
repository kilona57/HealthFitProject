from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Exercise, Workout, WorkoutExercise
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch


@login_required
def workout_list(request):
    workouts = Workout.objects.filter(created_by=request.user).prefetch_related(
        Prefetch('workoutexercise_set', queryset=WorkoutExercise.objects.select_related('exercise'))
    )
    return render(request, 'workout_list.html', {'workouts': workouts})


@login_required
def workout_detail(request, workout_id):
    arr = []
    workout = get_object_or_404(Workout, id=workout_id)
    workout_exercises = WorkoutExercise.objects.filter(workout=workout).select_related('exercise').order_by('order')
    context = {
        'workout_exercises': workout_exercises,
    }
    return render(request, 'workout_detail.html', context)


@login_required
def edit_workout(request, workout_id):
    workout = get_object_or_404(Workout, id=workout_id, created_by=request.user)
    exercises = Exercise.objects.all()
    workout_exercises = WorkoutExercise.objects.filter(workout=workout).select_related('exercise')

    return render(request, 'edit_workout.html', {
        'workout': workout,
        'exercises': exercises[:20],
        'workout_exercises': workout_exercises
    })


@login_required
def update_workout(request, workout_id):
    if request.method == 'POST':
        workout = get_object_or_404(Workout, id=workout_id, created_by=request.user)
        workout.name = request.POST.get('name')
        workout.description = request.POST.get('description')
        workout.difficulty_level = request.POST.get('difficulty_level')
        workout.save()
        return JsonResponse({'status': 'success'})


@login_required
def delete_workout_exercise(request, workout_id, exercise_id):
    if request.method == 'POST':
        WorkoutExercise.objects.filter(
            workout_id=workout_id,
            exercise_id=exercise_id,
            workout__created_by=request.user
        ).delete()
        return JsonResponse({'status': 'success'})