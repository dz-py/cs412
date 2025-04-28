from django.contrib import admin

# Register your models here.
from .models import Profile, Exercise, WorkoutSession, WorkoutEntry, Set

class SetInline(admin.TabularInline):
    model = Set
    extra = 1  # Number of empty forms to display
    fields = ['set_number', 'reps', 'weight']

@admin.register(WorkoutEntry)
class WorkoutEntryAdmin(admin.ModelAdmin):
    list_display = ['exercise', 'session', 'get_total_sets']
    list_filter = ['exercise', 'session']
    inlines = [SetInline]

    def get_total_sets(self, obj):
        return obj.sets.count()
    get_total_sets.short_description = 'Total Sets'

admin.site.register(Profile)
admin.site.register(Exercise)
admin.site.register(WorkoutSession)
