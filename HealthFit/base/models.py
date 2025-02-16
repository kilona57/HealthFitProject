from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Exercise(models.Model):
    name = models.CharField(max_length=300)
    description = models.TextField()
    muscle_group = models.CharField(max_length=100)
    difficulty = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], null=True
    )
    demonstration_video = models.URLField(blank=True, null=True, max_length=500)
    demonstration_video_2 = models.URLField(blank=True, null=True, max_length=500)
    calories = models.FloatField()
    equipment = models.CharField(max_length=100)

    class Meta:
        app_label = 'base'
    def __str__(self):
        return self.name


class Workout(models.Model):
    name = models.CharField(max_length=200, null=True)
    description = models.TextField(null=True)
    musle_group = models.CharField(max_length=200, null=True)
    equipment = models.CharField(max_length=200, null=True)
    difficulty_level = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], null=True
    )
    exercises = models.ManyToManyField(Exercise, through='WorkoutExercise')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class WorkoutExercise(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    sets = models.IntegerField()
    reps = models.IntegerField()
    rest_time_seconds = models.IntegerField()
    order = models.IntegerField()
    calories = models.FloatField()

    class Meta:
        ordering = ['order']


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sex = models.CharField(max_length=200, null=True)
    height = models.FloatField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    desired_weight = models.FloatField(null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    fitness_goal = models.CharField(max_length=200)
    additional_fitness_goals = models.CharField(max_length=700, null=True)
    activity = models.CharField(max_length=200, null=True)
    type_of_food = models.CharField(max_length=200, null=True)
    chest = models.IntegerField(null=True, blank=True)
    waist = models.IntegerField(null=True, blank=True)
    hips = models.IntegerField(null=True, blank=True)
    leg_in_thigh = models.IntegerField(null=True, blank=True)
    arm = models.IntegerField(null=True, blank=True)


class MealGroups(models.Model):
    group_name = models.CharField(max_length=500)


class Products(models.Model):
    products_name = models.CharField(max_length=500)
    protein_per_100g = models.FloatField()
    fat_per_100g = models.FloatField()
    carb_per_100g = models.FloatField()
    kcal_per_100g = models.FloatField()
    meal_groups = models.ManyToManyField(MealGroups, through='UserFood')


class UserFood(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    meal_group = models.ForeignKey(MealGroups, on_delete=models.CASCADE)
    gramming_product = models.IntegerField()
    kcal = models.FloatField()
    protein = models.FloatField()
    fat = models.FloatField()
    carb = models.FloatField()


class Recipes(models.Model):
    recipe_name = models.CharField(max_length=500)
    group = models.ForeignKey(MealGroups, on_delete=models.CASCADE)
    preparation_time = models.CharField(max_length=500)
    number_of_portions = models.IntegerField()
    weight_portion = models.CharField(max_length=500)
    kcal_per_100g = models.FloatField()
    protein_per_100g = models.FloatField()
    fat_per_100g = models.FloatField()
    carb_per_100g = models.FloatField()
    image = models.URLField(blank=True, null=True, max_length=500)


class Ingredients(models.Model):
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE)
    ingredient_name = models.CharField(max_length=500)
    gramming = models.CharField(max_length=500)


class CookingSteps(models.Model):
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE)
    step = models.TextField()


class Water(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    water = models.IntegerField()


class TargetNutrition(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    target_kcal = models.FloatField()
    target_protein = models.FloatField()
    target_fat = models.FloatField()
    target_carb = models.FloatField()
    target_water = models.FloatField()