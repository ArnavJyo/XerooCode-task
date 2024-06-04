from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.github_login, name='github_login'),
    path('callback/', views.github_callback, name='github_callback'),
    path('repository_details/', views.display_repository_details, name='repository_details'),
    path('', views.hello_world,name='hello_world')
]
