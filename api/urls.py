from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views


app_name = 'api'


urlpatterns=[
    path('',views.home_view, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/',views.profile_view, name='profile'),
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),
    path('myposts/',views.my_posts, name='my_posts'),
]