from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    username = None
    first_name = models.CharField(max_length=50, verbose_name='first name')
    email = models.EmailField(unique=True, verbose_name='email address')
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email


class Gender(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Название')
    code = models.CharField(max_length=1, unique=True, verbose_name='Код')

    class Meta:
        verbose_name = 'Пол'
        verbose_name_plural = 'Пол'

    def __str__(self):
        return self.name


class ActivityType(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Название')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Вид активности'
        verbose_name_plural = 'Виды активности'

    def __str__(self):
        return self.name


class MainGoal(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название')

    class Meta:
        verbose_name = 'Главная цель'
        verbose_name_plural = 'Главные цели'

    def __str__(self):
        return self.name


class TypeFood(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Тип питания'
        verbose_name_plural = 'Типы питания'

    def __str__(self):
        return self.name


class AdditionalGoal(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название')

    class Meta:
        verbose_name = 'Дополнительная цель'
        verbose_name_plural = 'Дополнительные цели'

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    gender = models.ForeignKey(Gender, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Пол')
    date_of_birth = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    height = models.FloatField(null=True, blank=True, verbose_name='Рост')
    height_unit = models.CharField(
        max_length=10,
        choices=[('cm', 'Сантиметры'), ('ft', 'Футы/дюймы')],
        default='cm',
        verbose_name='Единица измерения роста'
    )

    weight = models.FloatField(null=True, blank=True, verbose_name='Вес')
    weight_unit = models.CharField(
        max_length=10,
        choices=[('kg', 'Килонраммы'), ('ld', 'Фунты')],
        verbose_name='Единица измерения веса'
    )
    desired_weight = models.FloatField(null=True, blank=True, verbose_name='Желаемый вес')
    activity_type = models.ForeignKey(ActivityType, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Главная цель')
    main_goal = models.ForeignKey(MainGoal, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Главная цель')
    type_food = models.ForeignKey(TypeFood, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Тип питания')
    additional_goal = models.ManyToManyField(AdditionalGoal, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Дополнительные цели')

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'

    def __str__(self):
        return f"Профиль {self.user.email}"



