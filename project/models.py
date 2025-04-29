# project/models.py
#
# This file contains the data models for the project app.
# It defines the structure of the database tables and their relationships.

from django.db import models
from django.contrib.auth.models import User

class Exercise(models.Model):
    """ Model for storing exercise information """
    name = models.CharField(max_length=100)  # Name of the exercise (e.g., "Bench Press", "Squats")
    muscle_group = models.CharField(max_length=50)  # Primary muscle group targeted (e.g., "Chest", "Legs")
    equipment = models.CharField(max_length=50)  # Equipment needed (e.g., "Dumbbell", "Barbell", "Bodyweight")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

class WorkoutSession(models.Model):
    """ Model for storing workout session information """
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Changed from Profile to User
    date = models.DateField()  # When the workout was performed
    notes = models.TextField(blank=True, null=True)  # Optional notes about the workout session

    def __str__(self):
        return f"{self.user.username}'s workout on {self.date}"

class WorkoutEntry(models.Model):
    """
    Represents a specific exercise performed during a workout session.
    Links to the exercise and contains the sets performed.
    """
    session = models.ForeignKey(WorkoutSession, on_delete=models.CASCADE)  # Link to the workout session
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)  # Link to the exercise performed

    def __str__(self):
        return f"{self.exercise.name}"

class Set(models.Model):
    """
    Represents a single set of an exercise in a workout entry.
    Contains the number of repetitions and weight used for this specific set.
    """
    workout_entry = models.ForeignKey(WorkoutEntry, on_delete=models.CASCADE, related_name='sets')
    reps = models.PositiveIntegerField()  # Number of repetitions for this set
    set_number = models.PositiveIntegerField()  # Which set number this is (1st, 2nd, etc.)
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # Weight used in pounds for this set

    class Meta:
        ordering = ['set_number']  # Order sets by set number

    def __str__(self):
        return f"Set {self.set_number}: {self.reps} reps @ {self.weight}lbs"
