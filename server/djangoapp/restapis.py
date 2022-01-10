import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

# GET request
def get_request(url, **kwargs):
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
        status_code = response.status_code
        if status_code == 200:
            json_data = json.loads(response.text)
            # logger.log(logging.ERROR,json_data)
            return json_data
    except:
        # If any error occurs
        print("Network exception occurred")

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, payload, **kwargs):
    pass

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
            if 'purchase_date' in review_doc.keys():
                review_object = DealerReview(car_make=review_doc['car_make'], car_model=review_doc['car_model'], car_year=review_doc['car_year'],
                                         dealership=review_doc['dealership'], id=review_doc['id'], name=review_doc['name'],
                                         purchase=review_doc['purchase'], review=review_doc['review'], purchase_date=review_doc['purchase_date'])
            else:
                review_object = DealerReview(car_make=review_doc['car_make'], car_model=review_doc['car_model'], car_year=review_doc['car_year'],
                                         dealership=review_doc['dealership'], id=review_doc['id'], name=review_doc['name'],
                                         purchase=review_doc['purchase'], review=review_doc['review'])
            results.append(review_object)
    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(text):
    pass
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative



