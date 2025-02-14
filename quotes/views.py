from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import random


quotes = [
    "Innovation distinguishes between a leader and a follower.",
    "Design is not just what it looks like and feels like. Design is how it works.",
    "Be a yardstick of quality. Some people aren't used to an environment where excellence is expected.",
    "Sometimes life is going to hit you in the head with a brick. Don't lose faith.",
    "Your time is limited, so don't waste it living someone else's life.",
    "Stay hungry, stay foolish.",
    "The people who are crazy enough to think they can change the world are the ones who do.",
    "Quality is more important than quantity. One home run is much better than two doubles.",
]
images = [
    "https://media.wired.com/photos/592687718d4ebc5ab806a98d/master/pass/apple-steve-jobs-iphone-AP_070109066608.jpg",
    "https://mg.co.za/wp-content/uploads/2023/03/stevejobs.1419962519.jpeg",
    "https://media-cldnry.s-nbcnews.com/image/upload/newscms/2017_11/1931851/170313-steve-jobs-mn-1716-1931851.jpg",
    "https://www.tuaw.com/wp-content/uploads/2024/12/Steve-jobs.jpg",
]
# Create your views here.
def quote(request):
    ''' 
    The view for the main page.
    This view directs the application to display one quote and one image.
    The view will need to select one of each of these at random, and set them as context variables for use in the HTML template.
    Finally, it will delegate work to the quote.html template for display 
    '''
    response = 'quotes/quote.html'

    context = {
        'quote': random.choice(quotes),
        'image': random.choice(images),
    }
    return render(request, response, context)


def show_all(request):
    ''' The view to show all quotes '''
    response = 'quotes/show_all.html'
    context = {
        'quote': quotes,
        'image': images,
    }
    return render(request, response, context)


def about(request):
    ''' The view to display information about the famous person whose quotes are shown in this application '''
    response = 'quotes/about.html'
    return render(request, response)
