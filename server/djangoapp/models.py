from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField, DateField, IntegerField, TextField
from django.db.models.fields.related import ForeignKey, create_many_to_many_intermediary_model
from django.utils.timezone import now


# Create your models here.

# car make model
class CarMake(models.Model):
    name = CharField(max_length=100)
    description = TextField()

    def __str__(self):
        return self.name + " (" + self.description + ")"


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
class CarModel(models.Model):
    car_make = ForeignKey(CarMake, on_delete=CASCADE)
    name = CharField(max_length=100)
    dealer_id = IntegerField() # dealer created in cloudant database
    SEDAN, SUV, WAGON = 'SE', 'SU', 'WA'
    CAR_TYPE_CHOICES = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'WAGON')
    ]
    type = CharField(max_length=2,choices=CAR_TYPE_CHOICES)
    year = DateField()

    def __str__(self):
        return "Car " + self.name + " made by " + self.car_make + "of type" + self.type + \
            " selled on " + self.year + " with dealer " + self.dealer_id

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:
    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        self.address = address
        self.city = city
        self.full_name = full_name
        self.id = id
        self.lat = lat
        self.long = long
        self.short_name = short_name
        self.st = st
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    def __init__(self, car_make, car_model, car_year, dealership, id, name, purchase, review, purchase_date=None):
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.dealership = dealership
        self.id = id
        self.name = name
        self.purchase = purchase
        self.purchase_date = purchase_date
        self.review = review
    
    def __str__(self):
        return "Review by " + self.name + " with dealer " + self.dealership + " with car model " + self.car_model