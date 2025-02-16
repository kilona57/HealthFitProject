from django.shortcuts import render
from .models import Exercise
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Exercise, Workout, WorkoutExercise


@login_required
def view_exercises(request):
    exercises = Exercise.objects.all()
    return render(request, 'Тренировки copy.html', {'exercises': exercises[:20]})
