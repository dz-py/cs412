from django.urls import path
from . import views

app_name = 'project'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('exercises/', views.ExerciseListView.as_view(), name='exercise_list'),
    path('exercises/<int:pk>/', views.ExerciseDetailView.as_view(), name='exercise_detail'),
    path('workouts/', views.WorkoutSessionListView.as_view(), name='workout_session_list'),
    path('workouts/<int:pk>/', views.WorkoutSessionDetailView.as_view(), name='workout_session_detail'),
]
