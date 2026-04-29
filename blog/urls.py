from django.urls import path
from . import views


app_name='blog'
urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/delete/',views.post_delete, name='post_delete'),
    # path('tag/<str:tag_slug>/', views.post_tag, name='post_tag'),
    # path('category/<str:slug>/',views.post_category, name='post_category')
    path('comment/<int:pk>/edit/',views.edit_comment, name='edit_comment'),
    path('comment/<int:pk>/delete/',views.delete_comment, name='delete_comment'),
    path('profile/<str:username>/',views.user_profile, name='user_profile'),
    path('about/',views.about, name='about'),
]