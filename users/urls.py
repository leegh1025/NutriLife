from django.urls import path
from . import views


from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.user_info_goal, name='user_info_goal'),
    path('user_info/goal/', views.user_info_goal, name='user_info_goal'),
    path('user_info/count/', views.user_info_count, name='user_info_count'),
    path('user_info/basic/', views.user_info_basic, name='user_info_basic'),
    path('user_info/additional/', views.user_info_additional, name='user_info_additional'),
    path('user_info/sleep_duration/', views.user_info_sleep_duration, name='user_info_sleep_duration'),
    path('user_info/lifestyle/', views.user_info_lifestyle, name='user_info_lifestyle'),
    path('user_info/exercise/', views.user_info_exercise, name='user_info_exercise'),
    path('user_info/exercise_intensity/', views.user_info_exercise_intensity, name='user_info_exercise_intensity'),
    path('user_info/exercise_time/', views.user_info_exercise_time, name='user_info_exercise_time'),
    path('user_info/complete/', views.user_info_complete, name='user_info_complete'),
    path('user_info/results/', views.user_info_results, name='user_info_results'),
    path('user_info/refresh_meals/', views.refresh_meals, name='refresh_meals'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)