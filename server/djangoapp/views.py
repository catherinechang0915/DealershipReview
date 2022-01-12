from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)

# base url for cloud function endpoints
base_url = 'https://1c324d1e.us-south.apigw.appdomain.cloud/api/'

# Create an `about` view to render a static about page
def about(request):
    return render(request, 'djangoapp/about.html')


# Create a `contact` view to return a static contact page
def contact(request):
    return render(request, 'djangoapp/contact.html')

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    # Handles POST request
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['psw']
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            return redirect('djangoapp:index')
        else:
            # If not, return to login page again
            context['message'] = 'Invalid user. Please check your username and password.'
            return render(request, 'djangoapp/login.html', context)
    else:
        return render(request, 'djangoapp/login.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
    
        if not user_exist:
            # create and login new user
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            # redirect to login page for existing user
            context['message'] = "User already exists."
            return render(request, 'djangoapp/login.html', context)

# # Update the `get_dealerships` view to render the index page with a list of dealerships
# def get_dealerships(request):
#     context = {}
#     if request.method == "GET":
#         return render(request, 'djangoapp/index.html', context)

def get_dealerships(request):
    if request.method == "GET":
        url = base_url + 'dealership/'
        # Get dealers from the URL
        dealers = get_dealers_from_cf(url)
        # Return a list of dealer short name
        return render(request, 'djangoapp/index.html', {'dealers':dealers})

def get_dealerships_by_state(request, state):
    if request.method == 'GET':
        url = base_url + 'dealership/?state=' + str(state)
        dealers = get_dealers_from_cf(url, state=state)
        return render(request, 'djangoapp/index.html', {'dealers':dealers})

# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        url = base_url + 'review/?dealerId=' + str(dealer_id)
        reviews = get_dealer_reviews_from_cf(url, dealer_id=dealer_id)
        return render(request, 'djangoapp/dealer_details.html', {'reviews':reviews, 'dealer_id':dealer_id})

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    user = request.user
    if user.is_authenticated:
        url = base_url + 'review'
        review = dict()
        review['id'] = 1234
        review['name'] = 'test'
        review['dealership'] = 1
        review['review'] = 'The service for this dealership is very great!'
        review['purchase'] = False
        review['car_make'] = 'Audi'
        review['car_model'] = 'Car'
        review['car_year'] = 2020
        json_payload = dict()
        json_payload['review'] = review
        result = post_request(url, json_payload, dealer_id=dealer_id)
        logger.log(logging.ERROR, result)
        return HttpResponse(result)
