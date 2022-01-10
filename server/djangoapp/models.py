from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField, DateField, IntegerField, TextField
from django.db.models.fields.related import ForeignKey
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


# <HINT> Create a plain Python class `DealerReview` to hold review data
