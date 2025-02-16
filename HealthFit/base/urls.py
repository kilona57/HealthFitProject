from django.urls import path
from . import views, create_own_workout, view_and_edit_workouts, view_exercises, ai_workout_generation, food
# from . import views, create_own_workout, view_and_edit_workouts, view_exercises,  food
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.main_page_for_logout_user, name ='main_page_for_logout_user'),
    path('registration/', views.RegistrationView.as_view(), name ='registration'),
    path('login/', views.login_user, name ='login'),
    path('logout/', views.user_logout, name ='logout'),

    path('userinfo/', views.AddBodyParams.as_view(), name='userinfo'),
    path('view_exercises/', view_exercises.view_exercises, name='view_exercises'),
    path('create_workout/', create_own_workout.create_workout, name='create_workout'),
    path('add_exercise_to_workout/', create_own_workout.add_exercise_to_workout, name='add_exercise_to_workout'),
    path('workouts/', view_and_edit_workouts.workout_list, name='workout_list'),
    path('workout/edit/<int:workout_id>/', view_and_edit_workouts.edit_workout, name='edit_workout'),
    path('workout/update/<int:workout_id>/', view_and_edit_workouts.update_workout, name='update_workout'),
    path('workout/<int:workout_id>/delete-exercise/<int:exercise_id>/', view_and_edit_workouts.delete_workout_exercise, name='delete_workout_exercise'),
    path('workout/<int:workout_id>/', view_and_edit_workouts.workout_detail, name='workout_detail'),
    path('generate_workout/', ai_workout_generation.generate_workout, name='generate_workout'),

    path('profile/', views.profile_view, name='profile'),
    path('add_body_params/', views.add_body_params, name='add_body_params'),

    path('view_dairy/', views.view_dairy, name='view_dairy'),
    # # path('search_products/', food.search_products, name='search_products'),
    # # path('add_user_food/', food.add_user_food, name='add_user_food'),
    path('meal-groups/', food.choose_mealgroup, name='choose_mealgroup'),
    path('search_products/<int:mealgroup_id>/', food.search_and_add_product, name='search_products'),
    path('add_water/', food.add_water, name ='add_water'),
    path('view_recipes/', food.view_recipes, name='view_recipes'),
    path('view_recipes_breakfast/', food.view_recipes_breakfast, name='view_recipes_breakfast'),
    path('view_recipes_lunch/', food.view_recipes_lunch, name='view_recipes_lunch'),
    path('view_recipes_snack/', food.view_recipes_snack, name='view_recipes_snack'),
    path('view_recipes_dinner/', food.view_recipes_dinner, name='view_recipes_dinner'),
    path('view_recipe_steps/<int:recipe_id>/', food.view_recipe_steps, name='view_recipe_steps'),
    path('add_target_nutritions/', food.target_nutritions, name='add_target_nutritions')
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)