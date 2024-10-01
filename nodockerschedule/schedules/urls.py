from django.urls import path
from .views import home, create_schedule, schedule_detail
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('schedules/', views.create_schedule, name='schedules'),
    path('', views.home, name='home'),  # Это ваш путь к главной странице
    path('', home, name='home'),  # Главная страница
    path('create/', create_schedule, name='create_schedule'),
    path('<int:schedule_id>/', schedule_detail, name='schedule_detail'),
]