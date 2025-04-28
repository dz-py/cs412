from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from .models import Exercise, WorkoutSession, WorkoutEntry

# Create your views here.

class HomeView(TemplateView):
    template_name = 'project/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_workouts'] = WorkoutSession.objects.order_by('-date')[:5]
        context['exercise_count'] = Exercise.objects.count()
        return context

class ExerciseListView(ListView):
    model = Exercise
    template_name = 'project/exercise_list.html'
    context_object_name = 'exercises'

class ExerciseDetailView(DetailView):
    model = Exercise
    template_name = 'project/exercise_detail.html'
    context_object_name = 'exercise'

class WorkoutSessionListView(ListView):
    model = WorkoutSession
    template_name = 'project/workout_session_list.html'
    context_object_name = 'workout_sessions'

class WorkoutSessionDetailView(DetailView):
    model = WorkoutSession
    template_name = 'project/workout_session_detail.html'
    context_object_name = 'workout_session'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['workout_entries'] = WorkoutEntry.objects.filter(session=self.object)
        return context
