# restaurant/views.py
# This file contains the views for WcDonald's webapp.
# It includes views for the main page, order page, and order confirmation page.
# The main page displays the restaurant image, the order page shows a daily special,
# and the confirmation page processes the order form and calculates the total price.

from django.shortcuts import render
import random
from django.utils import timezone
from datetime import datetime, timedelta

restaurant_img = "https://media-cldnry.s-nbcnews.com/image/upload/rockcms/2024-03/wcdonalds-today-1-sk-240309-5fb6af.jpg"
daily_specials = ['Big Wac', 'Quarter Pouncer', 'WcDuffle', 'WcChicken', 
                 'Filet-O-Finch', 'Egg WcWuzzle', 'WcHotcakes', 'WcFries', 
                 'WcFluffy', 'Sausage WcFluffin']

def main(request):
    ''' The view for the main page. '''
    response = "restaurant/main.html"
    context = {
        'image': restaurant_img
    }
    return render(request, response, context)


def order(request):
    ''' The view for the order page. '''
    response = "restaurant/order.html"

    # Select a random daily special
    daily_special = random.choice(daily_specials)
    request.session['daily_special'] = daily_special
    context = {
        'daily_special': daily_special
    }
    return render(request, response, context)


def confirmation(request):
    ''' Process the form submission and generate a list of items ordered '''
    response = 'restaurant/confirmation.html'
    if request.method == 'POST':
        # Get daily special from session
        daily_special_name = request.session.get('daily_special', '')

        # Get form data
        context = {
            'name': request.POST.get('name'),
            'phone': request.POST.get('phone'),
            'email': request.POST.get('email'),
            'special_instructions': request.POST.get('special_instructions'),
            
            # Check which items were ordered
            'burger': 'burger' in request.POST,
            'bigburger': 'bigburger' in request.POST,
            'bigburger_no_pickle': 'bigburger_no_pickle' in request.POST, 
            'fries': 'fries' in request.POST,
            'drink': 'drink' in request.POST,
            'daily_special': 'daily_special' in request.POST,
            'daily_special_name': daily_special_name,
        }
        
        # Calculate total price
        total = 0
        if context['burger']: total += 8
        if context['bigburger']: total += 10
        if context['fries']: total += 4
        if context['drink']: total += 2
        if context['daily_special']: total += 0 
        
        context['total_price'] = total
        
        # Generate a random ready time (30-60 minutes from now)
        current_time = timezone.now()
        minutes_to_add = random.randint(30, 60)
        ready_time = current_time + timedelta(minutes=minutes_to_add)
        context['ready_time'] = ready_time.strftime("%I:%M %p")
        
        return render(request, response, context)
