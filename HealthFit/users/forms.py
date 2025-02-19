from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from .models import CustomUser, UserProfile
import re
from datetime import date


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')
    first_name = forms.CharField(required=True, label='First Name')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Подтверждение пароля')

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'password', 'confirm_password']

    def matching_passwords(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('Папроли не совпадают')
        return confirm_password

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError('Пароль должен содержать не менее 8 символов.')
        if not re.search(r'[A-Za-z0-9!@#$%^&*(),.?":{}|<>]', password):
            raise forms.ValidationError('Пароль должен содержать символы A-Z, a-z, (!@#$%^&*(),.?":{}|<>)')
        return password


class LoginForm(AuthenticationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'autofocus': True}), label='Email')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')

    class Meta:
        fields = ['email', 'password']

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            user = authenticate(request=self.request, email=email, password=password)
            if user is None:
                raise forms.ValidationError('Неверный email или пароль.')
            return self.cleaned_data


class UserProfileForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'data'}),
        label='Date of birth',
        required=False)

    class Meta:
        model = UserProfile
        fields = ['gender', 'date_of_birth',
                  'height', 'height_unit',
                  'weight', 'weight_unit',
                  'department', 'activity_type',
                  'main_goal', 'type_food',
                  'additional_goal']

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get('date_of_birth')
        if date_of_birth and date_of_birth >= date.today():
            raise forms.ValidationError('Дата рождения не может быть больше текущей даты.')
        return date_of_birth
