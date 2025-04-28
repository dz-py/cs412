from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from .models import Exercise, WorkoutSession, WorkoutEntry
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import SignUpForm, ExerciseForm, WorkoutSessionForm
from django.urls import reverse_lazy

# Create your views here.

class HomeView(TemplateView):
    template_name = 'project/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['recent_workouts'] = WorkoutSession.objects.filter(user=self.request.user).order_by('-date')[:5]
            context['exercise_count'] = Exercise.objects.filter(user=self.request.user).count()
        else:
            context['recent_workouts'] = None
            context['exercise_count'] = None
        context['user'] = self.request.user
        return context

class ExerciseListView(LoginRequiredMixin, ListView):
    model = Exercise
    template_name = 'project/exercise_list.html'
    context_object_name = 'exercises'

    def get_queryset(self):
        return Exercise.objects.filter(user=self.request.user)

class ExerciseDetailView(DetailView):
    model = Exercise
    template_name = 'project/exercise_detail.html'
    context_object_name = 'exercise'

class WorkoutSessionListView(LoginRequiredMixin, ListView):
    model = WorkoutSession
    template_name = 'project/workout_session_list.html'
    context_object_name = 'workout_sessions'

    def get_queryset(self):
        return WorkoutSession.objects.filter(user=self.request.user)

class WorkoutSessionDetailView(LoginRequiredMixin, DetailView):
    model = WorkoutSession
    template_name = 'project/workout_session_detail.html'
    context_object_name = 'workout_session'

    def get_queryset(self):
        return WorkoutSession.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['workout_entries'] = WorkoutEntry.objects.filter(session=self.object)
        return context

class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('project:login')
    template_name = 'project/signup.html'

class ExerciseCreateView(LoginRequiredMixin, CreateView):
    model = Exercise
    form_class = ExerciseForm
    template_name = 'project/exercise_form.html'
    success_url = reverse_lazy('project:exercise_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ExerciseUpdateView(LoginRequiredMixin, UpdateView):
    model = Exercise
    form_class = ExerciseForm
    template_name = 'project/exercise_form.html'
    success_url = reverse_lazy('project:exercise_list')

    def get_queryset(self):
        return Exercise.objects.filter(user=self.request.user)

class ExerciseDeleteView(LoginRequiredMixin, DeleteView):
    model = Exercise
    template_name = 'project/exercise_confirm_delete.html'
    success_url = reverse_lazy('project:exercise_list')

    def get_queryset(self):
        return Exercise.objects.filter(user=self.request.user)

class WorkoutSessionCreateView(LoginRequiredMixin, CreateView):
    model = WorkoutSession
    form_class = WorkoutSessionForm
    template_name = 'project/workout_session_form.html'
    success_url = reverse_lazy('project:workout_session_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
