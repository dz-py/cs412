# project/urls.py
#
# This file contains URL patterns for the project app.
# It maps URLs to their corresponding views.

from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from .views import ProjectHomeView

app_name = 'project'

urlpatterns = [
    # Home page
    path('', ProjectHomeView.as_view(), name='project_home'),
    
    # Exercise-related URLs
    path('exercises/', views.ExerciseListView.as_view(), name='exercise_list'),
    path('exercises/<int:pk>/', views.ExerciseDetailView.as_view(), name='exercise_detail'),
    
    # Workout-related URLs
    path('workouts/', views.WorkoutSessionListView.as_view(), name='workout_session_list'),
    path('workouts/<int:pk>/', views.WorkoutSessionDetailView.as_view(), name='workout_session_detail'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('exercises/create/', views.ExerciseCreateView.as_view(), name='exercise_create'),
    path('exercises/<int:pk>/update/', views.ExerciseUpdateView.as_view(), name='exercise_update'),
    path('exercises/<int:pk>/delete/', views.ExerciseDeleteView.as_view(), name='exercise_delete'),
    path('workouts/create/', views.WorkoutSessionCreateView.as_view(), name='workout_session_create'),
    path('logout/', auth_views.LogoutView.as_view(next_page='project:home'), name='logout'),
    path('workouts/<int:pk>/delete/', views.WorkoutSessionDeleteView.as_view(), name='workout_session_delete'),
]
