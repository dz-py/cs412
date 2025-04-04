# voter_analytics/urls.py
# Defines the URL patterns for the voter analytics application
from django.urls import path
from .views import ShowRecords, VoterDetailView, VoterGraphsView

urlpatterns = [
    path('', ShowRecords.as_view(), name='voters'),
    path('voter/<int:pk>', VoterDetailView.as_view(), name='voter'),
    path('graphs', VoterGraphsView.as_view(), name='graphs'),
]