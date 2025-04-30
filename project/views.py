# project/views.py
#
# This file contains all the view functions and classes for the project app.
# It handles the logic for displaying pages and processing user input.

from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from .models import Exercise, WorkoutSession, WorkoutEntry, Set
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import SignUpForm, ExerciseForm, WorkoutSessionForm, WorkoutEntryFormSet, SetFormSet
from django.urls import reverse_lazy
from django.utils import timezone
from datetime import datetime
from calendar import month_name


class HomeView(TemplateView):
    ''' Display the home page with recent workouts and quick stats '''
    template_name = 'project/home.html'

    def get_context_data(self, **kwargs):
        ''' Add context data for the home page '''
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Add workout entry formsets
        if self.request.POST:
            context['workout_entry_formset'] = WorkoutEntryFormSet(
                self.request.POST,
                prefix='entries'
            )
            for i, form in enumerate(context['workout_entry_formset']):
                form.prefix = f'entries-{i}'
                form.set_formset = SetFormSet(
                    self.request.POST,
                    instance=form.instance,
                    prefix=f'sets-{i}'
                )
        else:
            context['workout_entry_formset'] = WorkoutEntryFormSet(
                prefix='entries'
            )
            for i, form in enumerate(context['workout_entry_formset']):
                form.prefix = f'entries-{i}'
                form.set_formset = SetFormSet(
                    instance=form.instance,
                    prefix=f'sets-{i}'
                )
        
        # Add workout stats
        if user.is_authenticated:
            context['recent_workouts'] = WorkoutSession.objects.filter(
                user=user
            ).order_by('-date')[:5]
            context['total_exercises'] = Exercise.objects.filter(user=user).count()
            context['total_workouts'] = WorkoutSession.objects.filter(user=user).count()
            context['total_sets'] = Set.objects.filter(workout_entry__session__user=user).count()
        else:
            context['recent_workouts'] = []
            context['total_exercises'] = 0
            context['total_workouts'] = 0
            context['total_sets'] = 0

        return context


class ExerciseListView(LoginRequiredMixin, ListView):
    ''' Display a list of all exercises with filtering options '''
    model = Exercise
    template_name = 'project/exercise_list.html'
    context_object_name = 'exercises'

    def get_queryset(self):
        ''' Return exercises filtered by muscle group if provided '''
        queryset = Exercise.objects.filter(user=self.request.user)
        muscle_group = self.request.GET.get('muscle_group')
        if muscle_group:
            queryset = queryset.filter(muscle_group__icontains=muscle_group)
        return queryset

    def get_context_data(self, **kwargs):
        ''' Add muscle group filter options to context '''
        context = super().get_context_data(**kwargs)
        context['muscle_groups'] = Exercise.objects.filter(
            user=self.request.user
        ).values_list('muscle_group', flat=True).distinct()
        return context


class ExerciseDetailView(LoginRequiredMixin, DetailView):
    ''' Display details of a specific exercise '''
    model = Exercise
    template_name = 'project/exercise_detail.html'
    context_object_name = 'exercise'


class WorkoutSessionListView(LoginRequiredMixin, ListView):
    ''' Display a list of all workout sessions with filtering options '''
    model = WorkoutSession
    template_name = 'project/workout_session_list.html'
    context_object_name = 'workout_sessions'

    def get_queryset(self):
        ''' Return workout sessions filtered by month and year '''
        queryset = WorkoutSession.objects.filter(user=self.request.user)
        month = self.request.GET.get('month')
        year = self.request.GET.get('year')
        
        if month and year:
            queryset = queryset.filter(date__year=year, date__month=month)
        elif month:
            queryset = queryset.filter(date__month=month)
        elif year:
            queryset = queryset.filter(date__year=year)
            
        return queryset.order_by('-date')

    def get_context_data(self, **kwargs):
        ''' Add months and years for filtering to context '''
        context = super().get_context_data(**kwargs)
        dates = WorkoutSession.objects.filter(user=self.request.user).dates('date', 'month').order_by('-date')
        context['months'] = [(i, month_name[i]) for i in range(1, 13)]
        context['years'] = sorted(set(date.year for date in dates), reverse=True)
        return context


class WorkoutSessionDetailView(LoginRequiredMixin, DetailView):
    ''' Display details of a specific workout session '''
    model = WorkoutSession
    template_name = 'project/workout_session_detail.html'
    context_object_name = 'workout_session'

    def get_queryset(self):
        ''' Return workout sessions owned by the current user '''
        return WorkoutSession.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        ''' Add workout entries and their sets to context '''
        context = super().get_context_data(**kwargs)
        context['workout_entries'] = WorkoutEntry.objects.filter(
            session=self.object
        ).select_related('exercise').prefetch_related('sets')
        return context


class SignUpView(CreateView):
    ''' View for user registration '''
    form_class = SignUpForm
    success_url = reverse_lazy('project:login')
    template_name = 'project/signup.html'


class ExerciseCreateView(LoginRequiredMixin, CreateView):
    ''' Create a new exercise '''
    model = Exercise
    form_class = ExerciseForm
    template_name = 'project/exercise_form.html'
    success_url = reverse_lazy('project:exercise_list')

    def form_valid(self, form):
        ''' Assign the logged-in user as owner of the exercise '''
        form.instance.user = self.request.user
        return super().form_valid(form)


class ExerciseUpdateView(LoginRequiredMixin, UpdateView):
    ''' Update an existing exercise '''
    model = Exercise
    form_class = ExerciseForm
    template_name = 'project/exercise_form.html'
    success_url = reverse_lazy('project:exercise_list')

    def get_queryset(self):
        ''' Only allow the user to update their own exercises '''
        return Exercise.objects.filter(user=self.request.user)


class ExerciseDeleteView(LoginRequiredMixin, DeleteView):
    ''' Delete an existing exercise '''
    model = Exercise
    template_name = 'project/exercise_confirm_delete.html'
    success_url = reverse_lazy('project:exercise_list')

    def get_queryset(self):
        ''' Only allow the user to delete their own exercises '''
        return Exercise.objects.filter(user=self.request.user)


class WorkoutSessionCreateView(LoginRequiredMixin, CreateView):
    ''' Create a new workout session with entries and sets '''
    model = WorkoutSession
    form_class = WorkoutSessionForm
    template_name = 'project/workout_session_form.html'
    success_url = reverse_lazy('project:workout_session_list')

    def get_context_data(self, **kwargs):
        ''' Add workout entry formsets to context '''
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['workout_entry_formset'] = WorkoutEntryFormSet(
                self.request.POST,
                prefix='entries',
                form_kwargs={'user': self.request.user}
            )
            for i, form in enumerate(context['workout_entry_formset']):
                form.prefix = f'entries-{i}'
                form.set_formset = SetFormSet(
                    self.request.POST,
                    instance=form.instance,
                    prefix=f'sets-{i}'
                )
        else:
            context['workout_entry_formset'] = WorkoutEntryFormSet(
                prefix='entries',
                form_kwargs={'user': self.request.user}
            )
            for i, form in enumerate(context['workout_entry_formset']):
                form.prefix = f'entries-{i}'
                form.set_formset = SetFormSet(
                    instance=form.instance,
                    prefix=f'sets-{i}'
                )
        return context

    def form_valid(self, form):
        ''' Save the workout session, entries, and sets '''
        context = self.get_context_data()
        workout_entry_formset = context['workout_entry_formset']

        if workout_entry_formset.is_valid():
            self.object = form.save(commit=False)
            self.object.user = self.request.user
            self.object.save()

            for i, workout_entry_form in enumerate(workout_entry_formset.forms):
                workout_entry = workout_entry_form.save(commit=False)
                workout_entry.session = self.object
                workout_entry.save()

                set_formset = SetFormSet(
                    self.request.POST,
                    instance=workout_entry,
                    prefix=f'sets-{i}'
                )

                if set_formset.is_valid():
                    sets = set_formset.save(commit=False)
                    for set_num, set_instance in enumerate(sets, start=1):
                        set_instance.set_number = set_num
                        set_instance.save()

            return redirect(self.get_success_url())

        # If invalid, re-render form
        return self.render_to_response(self.get_context_data(form=form))


class WorkoutSessionDeleteView(LoginRequiredMixin, DeleteView):
    ''' Delete an existing workout session '''
    model = WorkoutSession
    template_name = 'project/workout_session_confirm_delete.html'
    success_url = reverse_lazy('project:workout_session_list')

    def get_queryset(self):
        ''' Only allow the user to delete their own workout sessions '''
        return WorkoutSession.objects.filter(user=self.request.user)
