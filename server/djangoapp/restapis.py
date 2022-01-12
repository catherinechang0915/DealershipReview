import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import logging
import os

# Get an instance of a logger
logger = logging.getLogger(__name__)

# load env variables
load_dotenv()
NLU_API_KEY = os.environ.get('NLU_API_KEY')
NLU_API_URL = os.environ.get('NLU_API_URL')

# GET request
def get_request(url, **kwargs):
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs, auth=HTTPBasicAuth('apikey', NLU_API_KEY))
        status_code = response.status_code
        if status_code == 200:
            json_data = json.loads(response.text)
            return json_data
        else:
            logger.log(logging.ERROR, 'Get request at {} with params {} failed with status {}'.format(url, kwargs, status_code))
    except:
        # If any error occurs
        logger.log(logging.ERROR, "Network exception occurred")

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, payload, **kwargs):
    try:
        response = requests.post(url, json=payload)
        status_code = response.status_code
        if status_code == 200:
            json_data = json.loads(response.text)
            return json_data
        else:
            logger.log(logging.ERROR, 'Post request at {} with payload {} failed with status {}'.format(url, payload, status_code))
    except:
        logger.log(logging.ERROR, "Network exception occurred")

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, kwargs=kwargs)
    if json_result and 'status' not in json_result.keys():
        for dealer_doc in json_result['query']:
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)
    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    json_result = get_request(url, kwargs=kwargs)
    if json_result and 'status' not in json_result.keys():
        for review_doc in json_result['message']:
            review_object = DealerReview(car_make=review_doc.get('car_make'), car_model=review_doc.get('car_model'), car_year=review_doc.get('car_year'),
                                         dealership=review_doc.get('dealership'), id=review_doc.get('id'), name=review_doc.get('name'),
                                         purchase=review_doc.get('purchase'), review=review_doc.get('review'), purchase_date=review_doc.get('purchase_date'))
            review_object.sentiment = analyze_review_sentiments(review_object.review)
            results.append(review_object)
    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(text):
    params = dict()
    params["text"] = text
    params["version"] = "2021-08-01"
    params["features"] = "sentiment"
    result = get_request(NLU_API_URL, text=text, version="2021-08-01", features="sentiment")
    if result:
        sentiment = result['sentiment']['document']['label']
        # logger.log(logging.ERROR, sentiment)
        return sentiment
    else:
        return None
