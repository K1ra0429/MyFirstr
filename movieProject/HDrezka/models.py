from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.urls import reverse

class Category(models.Model):
    title = models.CharField(max_length=30, verbose_name=' Название категории', unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'


class Movie(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название фильма')
    descr = models.TextField(verbose_name='Описание')
    released = models.CharField(max_length=50, verbose_name='Дата выхода')
    country = models.TextField(verbose_name='Страна')
    director = models.CharField(max_length=50, verbose_name='Режисёр')
    translation = models.TextField(verbose_name='В переводе')
    age = models.IntegerField(default=0, verbose_name='Возраст')
    time = models.IntegerField(default=0, verbose_name='Время')
    actors = models.TextField(verbose_name='В ролях актеры')
    photo = models.ImageField(upload_to='media/moviesphoto/', verbose_name='Фото фильма')
    movie = models.FileField(upload_to='media/movies/', null=True, blank=True, verbose_name='Файл с фильмом')
    category = models.ManyToManyField(Category, verbose_name='Жанры')
    views = models.IntegerField(default=0, verbose_name='Просмотры')
    trailer = models.TextField(verbose_name='Трейлер')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')



    def __str__(self):
            return self.title

    def get_absolute_url(self):
        return reverse('movie', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'


class Comment(models.Model):
    text = models.CharField(max_length=350, verbose_name='Текст комментария')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name='Фильм')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    def __str__(self):
        return f'Комментарий к фильму "{self.movie.title}" от {self.author}'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

class Profile(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название профиля')
    profile_photo = models.ImageField(upload_to='media/profilephoto/', verbose_name='Фото профиля')
    email = models.EmailField(verbose_name='Почта пользователя')
    descr_profil = models.TextField(verbose_name='Описание профиля')
