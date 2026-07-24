from django.urls import path
from .views import *

urlpatterns = [
    path('', MovieListView.as_view(), name='main'),
    path('category/<int:pk>/', MovieByCategoryView.as_view(), name='category'),
    path('movie/<int:pk>/', MovieDetailView.as_view(), name='movie'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', logout_user_view, name='logout'),
    path('register/', register_user_view, name='register'),
    path('search/', SearchGame.as_view(), name='search'),
    path('comment/save/<int:pk>/', save_comment_user, name='comment_save'),
    path('comment/update/<int:pk>/', CommentUpdate.as_view(), name='comment_update'),
    path("profile/", ProfileView.as_view(), name="profile"),

]
