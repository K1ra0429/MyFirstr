
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, redirect
from .models import Category, Movie, Comment
from .forms import LoginForm, RegisterUserForm, CommentForm
from django.views.generic import ListView, DetailView, UpdateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse
from django.views.generic import TemplateView

# Create your views here.
# def main_page_view(request):
#     games = Game.objects.all().order_by('-created_at')
#
#     context = {
#         'title': 'качай и играй',
#         'games': games
#     }
#
#     return render(request, 'HDrezka/main.html', context)






class MovieListView(ListView):
    model = Movie
    context_object_name = 'movies'
    template_name = 'HDrezka/main.html'
    ordering = '-created_at'
    extra_context = {'title': 'Смотри в хорошем качестве'}


# =======================================================================
# Функция получения игр по id категории
# def game_by_category(request, pk):
#     games = Game.objects.filter(category=pk).order_by('-created_at')
#     cat = Category.objects.get(pk=pk)
#
#     context = {
#         'games': games,
#         'title': cat.title
#     }
#
#     return render(request, 'HDrezka/main.html', context)

class MovieByCategoryView(ListView):
    model = Movie
    context_object_name = 'movies'
    template_name = 'HDrezka/main.html'

    # Метод что бы переназначить вывод данных
    def get_queryset(self):
        movies = Movie.objects.filter(category=self.kwargs['pk']).order_by('-created_at')
        return movies

    # Метод что бы дополнительно что то отправить на страницу
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MovieByCategoryView, self).get_context_data()
        cat = Category.objects.get(pk=self.kwargs['pk'])
        context['title'] = cat.title
        return context


# =======================================================================
# Функция получения игры по id на сип=ранице детали
# def game_detail_view(request, pk):
#     if Game.objects.filter(pk=pk).exists():
#         game = Game.objects.get(pk=pk)
#         same_games = Game.objects.filter(category__in=game.category.all()).distinct().exclude(pk=pk)
#         context = {
#             'game': game,
#             'title': game.title,
#             'same_games': same_games.order_by('-created_at')[:3]
#         }
#
#         return render(request, 'HDrezka/game_detail.html', context)
#     else:
#         return redirect('main')

class MovieDetailView(DetailView):
    model = Movie
    context_object_name = 'movie'
    template_name = 'HDrezka/game_detail.html'

    def get_context_data(self, **kwargs):
        context = super(MovieDetailView, self).get_context_data()
        movie = context['movie']
        same_movies = Movie.objects.filter(category__in=movie.category.all()).distinct().exclude(pk=movie.pk)
        context['same_movies'] = same_movies.order_by('-created_at')[:3]
        context['title'] = movie.title
        context['comments'] = Comment.objects.filter(movie=movie).order_by('-created_at')
        context['form'] = CommentForm()
        return context


class LoginUserView(LoginView):
    form_class = LoginForm  # Форма для авторизации
    template_name = 'HDrezka/login.html'  # НА какой странице будет авторизация
    next_page = 'main'  # После авторизации куда перенаправит
    redirect_authenticated_user = 'main'  # Если Автороизован перенаправит на главную страницу
    extra_context = {'title': 'Авторизация'}


# =======================================================================
def logout_user_view(request):
    logout(request)
    return redirect('main')


def register_user_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            # логика регисрации данных пользователя
            form = RegisterUserForm(data=request.POST)  # Отправим в форму данные для сохраненния
            if form.is_valid():  # Проверим на валижность всё ли верно указали
                user = form.save()  # Форма сохранит данные и вернёт пользователя
                login(request, user)  # Выполним логинизацию
                return redirect('main')  # и перенаправим на главную старницу
        else:
            form = RegisterUserForm()

        context = {
            'title': 'Регистрация',
            'form': form
        }

        return render(request, 'HDrezka/register.html', context)

    else:
        return redirect('main')





class SearchGame(MovieListView):

    def get_queryset(self):
        word = self.request.GET.get('q')
        games = Movie.objects.filter(Q(title__iregex=word) | Q(descr__iregex=word)).order_by('-created_at')
        return games


def save_comment_user(request, pk):
    if request.method == 'POST' and request.user.is_authenticated:
        if Movie.objects.filter(pk=pk).exists():  # Проверяем сущ ли игра
            form = CommentForm(data=request.POST)  # В форму отправляем текст комменатрия
            if form.is_valid():
                comment = form.save(commit=False)  # commit=False  отложить сохранить
                comment.author = request.user  # Указали автора для коммента
                comment.movie = Movie.objects.get(pk=pk)  # Указали игру для коммента
                comment.save()

            return redirect('movie', pk=pk)
        else:
            return redirect('main')
    else:
        return redirect('login')



class CommentUpdate(LoginRequiredMixin, UpdateView):
    login_url = 'login'
    form_class = CommentForm
    model = Comment

    def get(self, request, *args, **kwargs):
        if Comment.objects.filter(pk=self.kwargs['pk'], author=request.user).exists():
            return super(CommentUpdate, self).get(request, *args, **kwargs)
        else:
            return redirect('main')

    def get_success_url(self):
        comment = Comment.objects.get(pk=self.kwargs['pk'])
        return reverse('movie', kwargs={'pk': comment.movie.pk})


class ProfileView(TemplateView):
    template_name = "HDrezka/profil.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context
