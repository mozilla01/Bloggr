from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout, name='logout'),
    path('create-post', views.create_post, name='create-post'),
    path('post/<str:pk>', views.post, name='post'),
    path('post/<str:pk>/edit-post', views.edit_post, name='edit-post'),
    path('post/<str:pk>/delete-post', views.delete_post, name='delete-post'),
]