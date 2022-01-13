from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect

from .models import CarModel
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

# global name correspondence
name_correspondence = None
with open('djangoapp/name_correspondence.json') as f:
    name_correspondence = json.load(f)

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
        dealer_name = name_correspondence[str(dealer_id)]
        return render(request, 'djangoapp/dealer_details.html', {'reviews':reviews, 'dealer_id':dealer_id, 'dealer_name':dealer_name})

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    def car_list(dealer_id):
        cars = []
        car_models = CarModel.objects.all()
        for car_model in car_models:
            if car_model.dealer_id == dealer_id:
                cars.append(car_model)
        return cars

    def find_car_by_id(car_id):
        car_models = CarModel.objects.all()
        for car_model in car_models:
            if car_model.id == car_id:
                return car_model

    def extract_review(request, dealer_id):
        params = request.POST
        review = dict()
        review['review'] = params['content']
        review['name'] = request.user.username
        review['dealership'] = dealer_id

        if params.get('purchasecheck'):
            review['purchase'] = True
            car_id = int(params['car'])
            car_model = find_car_by_id(car_id)
            review['car_make'] = car_model.car_make.name
            review['car_model'] = car_model.name
            review['car_year'] = int(car_model.year.strftime("%Y"))
            review['purchase_date'] = params['purchasedate']
        return review

    if request.method == 'GET':
        cars = car_list(dealer_id)
        dealer_name = name_correspondence[str(dealer_id)]
        return render(request, 'djangoapp/add_review.html', {'cars':cars, 'dealer_id':dealer_id, 'dealer_name':dealer_name})
    if request.method == 'POST':
        user = request.user
        if user.is_authenticated:
            url = base_url + 'review'
            review = extract_review(request, dealer_id)
            json_payload = dict()
            json_payload['review'] = review
            result = post_request(url, json_payload, dealer_id=dealer_id)
            return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
