# project/admin.py
#
# This file configures how models are displayed and managed in the Django admin interface.

from django.contrib import admin
from .models import Exercise, WorkoutSession, WorkoutEntry, Set

class SetInline(admin.TabularInline):
    ''' Define an inline admin interface for Set objects within a WorkoutEntry '''
    model = Set
    extra = 1  # Number of empty Set forms to display by default
    fields = ['set_number', 'reps', 'weight']  # Fields to display in the inline form

@admin.register(WorkoutEntry)
class WorkoutEntryAdmin(admin.ModelAdmin):
    ''' Define admin interface for WorkoutEntry model '''
    list_display = ['exercise', 'session', 'get_total_sets']  # Fields to display in the list view
    list_filter = ['exercise', 'session']  # Add filtering options in the sidebar
    inlines = [SetInline]  # Allow editing Sets directly within WorkoutEntry

    def get_total_sets(self, obj):
        ''' Return the total number of sets associated with this WorkoutEntry '''
        return obj.sets.count()
    get_total_sets.short_description = 'Total Sets'  # Column header in the admin list view

# Register Exercise and WorkoutSession models with default admin interface
admin.site.register(Exercise)
admin.site.register(WorkoutSession)
