from django.urls import path
from . import views

urlpatterns = [
    path('user_info/goal/', views.user_info_goal, name='user_info_goal'),
    path('user_info/count/', views.user_info_count, name='user_info_count'),
    path('user_info/basic/', views.user_info_basic, name='user_info_basic'),
    path('user_info/additional/', views.user_info_additional, name='user_info_additional'),
    path('user_info/sleep_duration/', views.user_info_sleep_duration, name='user_info_sleep_duration'),
]