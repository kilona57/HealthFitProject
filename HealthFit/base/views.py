from django.views.generic import TemplateView, View
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from .forms import CustomPasswordChangeForm
from .models import UserProfile, TargetNutrition
from django.utils import dateparse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import datetime
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages


class MainPageView(TemplateView):
    template_name = 'index.html'

    def post(self, request):
        if request.method == 'POST':
            # Дополнительная логика удаления аккаунта
            # Например, удаление пользователя из базы данных
            request.user.delete()
            logout(request)  # Выход пользователя после удаления аккаунта
            return redirect('login')  # Перенаправление на главную страницу после удаления
        return render(request, self.template_name)


class RegistrationView(View):
    template_name = 'Регистрация.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('name-f18c')
        email = request.POST.get('phone-cbff')
        password = request.POST.get('text-13a4')
        confirm_password = request.POST.get('message-1015')

        if password == confirm_password:
            validate_password(password)
            user = User.objects.create_user(username, email, password)
            user.save()
            login(request, user)
            print(username)
            # messages.success(request, 'You have successfully registered!')
            return JsonResponse({'redirect': '/userinfo/'})


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print(user)
            return JsonResponse({'redirect': '/profile/'})

        else:
            error_message = 'Incorrect email or password. Please try again.'
            return render(request, 'login_page.html', {'error_message': error_message})

    return render(request, 'login_page.html')


def user_logout(request):
    logout(request)
    return redirect('main_page_for_logout_user')


def main_page_for_logout_user(request):
    if request.user.is_authenticated:
        return render(request, 'index.html')
    else:
        return render(request, 'index_copy.html')


class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'password_change.html'
    success_url = reverse_lazy('login')


class AddBodyParams(View):
    template_name = 'Информация о пользователе.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        if request.method == 'POST':
            # user = authenticate(request, username=username, password=password)
            if request.user:
                sex = request.POST.get('select-b6e8')
                height = request.POST.get('text-74dd')
                weight = request.POST.get('text-c043')
                desired_weight = request.POST.get('text-bb48')
                birth_date = request.POST.get('text-e46f')
                birth_date = dateparse.parse_date(birth_date)
                fitness_goal = request.POST.get('select-bda1')
                additional_fitness_goals = request.POST.getlist('additional_fitness_goals')
                activity = request.POST.get('select-1016')
                additional_fitness_goals_str = ', '.join(additional_fitness_goals)
                type_of_food = request.POST.get('type_of_food')
                user = get_object_or_404(User, id=request.user.id)
                print(user)
                # Проверяем, существует ли уже профиль
                if UserProfile.objects.filter(user=user).exists():
                    return JsonResponse({'redirect': '/profile/'})

                user = UserProfile.objects.create(user=request.user, sex=sex, height=height, weight=weight,
                                                  desired_weight=desired_weight, birth_date=birth_date,
                                                  fitness_goal=fitness_goal,
                                                  additional_fitness_goals=additional_fitness_goals_str,
                                                  activity=activity, type_of_food=type_of_food)
                user.save()
                # login(request, user)
                return JsonResponse({'redirect': '/profile/'})

            else:
                error_message = 'Incorrect email or password. Please try again.'
                return render(request, self.template_name, {'error_message': error_message})
        else:

            return render(request, self.template_name)


def profile_view(request):
    user = get_object_or_404(UserProfile, user=request.user)
    # user_profile = UserProfile.objects.filter(user=user)
    user_activity = user.activity
    if user_activity.find('('):
        user_activity = user_activity[:user.activity.find('(')]
    print(user_activity)
    print(datetime.datetime.now().date())
    today = datetime.datetime.now().date()

    age = today.year - user.birth_date.year - ((today.month, today.day) < (user.birth_date.month, user.birth_date.day))
    print(user.weight)
    imt = round(user.weight / ((user.height / 100) ** 2), 2)
    print(imt)
    targer_nutritions = TargetNutrition.objects.filter(user=request.user).order_by('id').last()

    return render(request, 'Профиль.html',
                  {'age': age, 'activity': user_activity, 'type_of_food': user.type_of_food, 'weight': int(user.weight),
                   'name': request.user.username, 'goal': user.fitness_goal, 'desired_weight': int(user.desired_weight),
                   'imt': imt, 'targer_nutritions': targer_nutritions})


def add_body_params(request):
    user = get_object_or_404(UserProfile, user_id=request.user.id)
    if request.method == 'POST':
        chest = request.POST.get('chest')
        waist = request.POST.get('waist')
        hips = request.POST.get('hips')
        leg_in_thigh = request.POST.get('leg_in_thigh')
        arm = request.POST.get('arm')
        print(chest)
        user.chest = chest
        user.waist = waist
        user.hips = hips
        user.leg_in_thigh = leg_in_thigh
        user.arm = arm
        user.save()
        return JsonResponse({'status': 'success'})


def view_dairy(request):
    return render(request, 'dairy.html')
