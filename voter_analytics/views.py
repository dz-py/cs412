# voter_analytics/views.py
# Displays the list of voters, their details, and graphs for voter analytics.

from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Voter
import plotly.express as px
from django.db.models import Count
import pandas as pd
from datetime import datetime

class ShowRecords(ListView):
    '''Show the list of voters with filtering options'''
    model = Voter
    template_name = 'voter_analytics/voter_list.html'
    context_object_name = 'results'
    paginate_by = 100

    def get_queryset(self):
        '''Return the filtered queryset based on the request parameters'''
        qs = super().get_queryset()
        party = self.request.GET.get('party_affiliation')
        if party:
            qs = qs.filter(party_affiliation=party.strip())

        min_dob = self.request.GET.get('min_dob')
        if min_dob:
            qs = qs.filter(dob__gte=f"{min_dob}-01-01")

        max_dob = self.request.GET.get('max_dob')
        if max_dob:
            qs = qs.filter(dob__lte=f"{max_dob}-12-31")

        voter_score = self.request.GET.get('voter_score')
        if voter_score:
            qs = qs.filter(voter_score=int(voter_score))

        if self.request.GET.get('v20state') == 'TRUE':
            qs = qs.filter(v20state='TRUE')
        if self.request.GET.get('v21town') == 'TRUE':
            qs = qs.filter(v21town='TRUE')
        if self.request.GET.get('v21primary') == 'TRUE':
            qs = qs.filter(v21primary='TRUE')
        if self.request.GET.get('v22general') == 'TRUE':
            qs = qs.filter(v22general='TRUE')
        if self.request.GET.get('v23town') == 'TRUE':
            qs = qs.filter(v23town='TRUE')

        return qs

    def get_context_data(self, **kwargs):
        '''Add additional context data for the template'''
        context = super().get_context_data(**kwargs)
        context['party_choices'] = ['D ', 'R ', 'U ', 'J ', 'A ', 'CC ', 'X ',
                                    'L ', 'Q ', 'S ', 'FF ', 'G ', 'HH ', 'T ',
                                    'AA ', 'GG ', 'Z ', 'O ', 'P ', 'E ', 'V ',
                                    'H ', 'Y ', 'W ', 'EE ', 'K ']
        context['year_choices'] = range(1920, 2004)
        context['score_choices'] = range(0, 6)
        return context

class VoterDetailView(DetailView):
    '''Show the details of a single voter'''
    model = Voter
    template_name = 'voter_analytics/voter_detail.html'
    context_object_name = 'voter'

class VoterGraphsView(ListView):
    '''Show graphs for voter analytics with filtering options'''
    model = Voter
    template_name = 'voter_analytics/graphs.html'
    context_object_name = 'results'

    def get_queryset(self):
        '''Return the filtered queryset based on the request parameters'''
        qs = super().get_queryset()
        party = self.request.GET.get('party_affiliation')
        if party:
            qs = qs.filter(party_affiliation=party.strip())

        min_dob = self.request.GET.get('min_dob')
        if min_dob:
            qs = qs.filter(dob__gte=f"{min_dob}-01-01")

        max_dob = self.request.GET.get('max_dob')
        if max_dob:
            qs = qs.filter(dob__lte=f"{max_dob}-12-31")

        voter_score = self.request.GET.get('voter_score')
        if voter_score:
            qs = qs.filter(voter_score=int(voter_score))

        if self.request.GET.get('v20state') == 'TRUE':
            qs = qs.filter(v20state='TRUE')
        if self.request.GET.get('v21town') == 'TRUE':
            qs = qs.filter(v21town='TRUE')
        if self.request.GET.get('v21primary') == 'TRUE':
            qs = qs.filter(v21primary='TRUE')
        if self.request.GET.get('v22general') == 'TRUE':
            qs = qs.filter(v22general='TRUE')
        if self.request.GET.get('v23town') == 'TRUE':
            qs = qs.filter(v23town='TRUE')

        return qs

    def get_context_data(self, **kwargs):
        '''Add graphs and filter options to the context data for the template'''
        context = super().get_context_data(**kwargs)
        filtered_qs = self.get_queryset()  

        # Histogram of voters by birth year
        voters_with_dob = filtered_qs.exclude(dob__isnull=True)
        birth_years = []
        for voter in voters_with_dob:
            try:
                birth_year = int(voter.dob[:4])
                birth_years.append(birth_year)
            except (ValueError, TypeError):
                continue
        birth_year_data = pd.DataFrame({'Birth Year': birth_years})
        birth_year_fig = px.histogram(
            birth_year_data,
            x='Birth Year',
            nbins=168,
            labels={'Birth Year': 'Year of Birth', 'count': 'Number of Voters'},
            color_discrete_sequence=['#636EFA']
        )
        birth_year_fig.update_layout(
            bargap=0.1,
            xaxis=dict(
                tickmode='linear',
                dtick=10,
                range=[1920, 2005]
            )
        )
        birth_year_div = birth_year_fig.to_html(full_html=False)

        # Pie chart of voters by party affiliation
        party_data = filtered_qs.values('party_affiliation').annotate(count=Count('id'))
        party_fig = px.pie(
            party_data,
            names='party_affiliation',
            values='count',
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        party_fig.update_traces(textposition='inside', textinfo='percent+label')
        party_div = party_fig.to_html(full_html=False)

        # Bar chart of election participation
        election_data = {
            'Election': ['v20State', 'v21Town', 'v21Primary', 'v22General', 'v23Town'],
            'Voted': [
                filtered_qs.filter(v20state='TRUE').count(),
                filtered_qs.filter(v21town='TRUE').count(),
                filtered_qs.filter(v21primary='TRUE').count(),
                filtered_qs.filter(v22general='TRUE').count(),
                filtered_qs.filter(v23town='TRUE').count()
            ]
        }
        election_fig = px.bar(
            election_data,
            x='Election',
            y='Voted',
            labels={'Voted': 'Number of Voters', 'Election': 'Election Type'},
            color_discrete_sequence=['#4169E1']
        )
        election_div = election_fig.to_html(full_html=False)

        # Add graphs and filter options to context
        context['birth_year_graph'] = birth_year_div
        context['party_graph'] = party_div
        context['election_graph'] = election_div
        context['party_choices'] = ['D ', 'R ', 'U ', 'J ', 'A ', 'CC ', 'X ',
                                    'L ', 'Q ', 'S ', 'FF ', 'G ', 'HH ', 'T ',
                                    'AA ', 'GG ', 'Z ', 'O ', 'P ', 'E ', 'V ',
                                    'H ', 'Y ', 'W ', 'EE ', 'K ']
        context['year_choices'] = range(1920, 2004)
        context['score_choices'] = range(0, 6)
        
        return context