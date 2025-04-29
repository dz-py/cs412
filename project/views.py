from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from .models import Exercise, WorkoutSession, WorkoutEntry, Set
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import SignUpForm, ExerciseForm, WorkoutSessionForm, WorkoutEntryFormSet, SetFormSet
from django.urls import reverse_lazy

# Create your views here.

class HomeView(TemplateView):
    template_name = 'project/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get the current user
        user = self.request.user
        
        # Add workout entry formset context
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
        
        # Add stats context
        if user.is_authenticated:
            # Recent workouts
            context['recent_workouts'] = WorkoutSession.objects.filter(
                user=user
            ).order_by('-date')[:5]
            
            # Total exercises
            context['total_exercises'] = Exercise.objects.filter(
                user=user
            ).count()
            
            # Total workouts
            context['total_workouts'] = WorkoutSession.objects.filter(
                user=user
            ).count()
            
            # Total sets
            context['total_sets'] = Set.objects.filter(
                workout_entry__session__user=user
            ).count()
        else:
            context['recent_workouts'] = []
            context['total_exercises'] = 0
            context['total_workouts'] = 0
            context['total_sets'] = 0
            
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
        # Get all workout entries and prefetch their related sets
        context['workout_entries'] = WorkoutEntry.objects.filter(
            session=self.object
        ).select_related('exercise').prefetch_related('sets')
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

    def get_context_data(self, **kwargs):
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

        # If invalid
        return self.render_to_response(self.get_context_data(form=form))


class WorkoutSessionDeleteView(LoginRequiredMixin, DeleteView):
    model = WorkoutSession
    template_name = 'project/workout_session_confirm_delete.html'
    success_url = reverse_lazy('project:workout_session_list')

    def get_queryset(self):
        return WorkoutSession.objects.filter(user=self.request.user)
