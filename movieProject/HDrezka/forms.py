from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from .models import Comment


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите логин'
    }))

    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите пароль'
    }))

    error_messages = {"invalid_login": "Не верный логин или пароль " }


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Задайте логин', widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))

    password1 = forms.CharField(label='Придумайте пароль', widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))

    password2 = forms.CharField(label='Придумайте пароль', widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))

    first_name = forms.CharField(label='Ваше имя', widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))

    last_name = forms.CharField(label='Ваша фамилия', widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))

    email = forms.EmailField(label='Почта', widget=forms.EmailInput(attrs={
        'class': 'form-control'
    }))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')

class CommentForm(forms.ModelForm):
    text = forms.CharField(max_length=350, label='Оставить комменатрий', widget=forms.Textarea(attrs={
        'class': 'form-control bg-dark text-light border-light',
        'style': 'height: 100px;'
    }))

    class Meta:
        model = Comment
        fields = ('text', )

