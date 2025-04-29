# project/apps.py
#
# This file contains the configuration for the project app.
# It defines the app's name and default settings.

from django.apps import AppConfig


class ProjectConfig(AppConfig):
    """ Configuration class for the project app """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'project'
