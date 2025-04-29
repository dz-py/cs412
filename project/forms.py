from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import inlineformset_factory
from .models import Exercise, WorkoutSession, WorkoutEntry, Set

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ['name', 'muscle_group', 'equipment']

class WorkoutEntryForm(forms.ModelForm):
    class Meta:
        model = WorkoutEntry
        fields = ['exercise']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['exercise'].queryset = Exercise.objects.filter(user=user)

class SetForm(forms.ModelForm):
    class Meta:
        model = Set
        fields = ['set_number', 'reps', 'weight']

WorkoutEntryFormSet = inlineformset_factory(
    WorkoutSession, 
    WorkoutEntry, 
    form=WorkoutEntryForm, 
    extra=1,
    can_delete=False
)

SetFormSet = inlineformset_factory(
    WorkoutEntry,
    Set,
    form=SetForm,
    extra=1,
    can_delete=False
)

class WorkoutSessionForm(forms.ModelForm):
    class Meta:
        model = WorkoutSession
        fields = ['date', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={
                'rows': 3,
                'cols': 40,
                'class': 'form-control',
                'placeholder': 'Optional notes about your workout...'
            }),
        } 