from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from cities_light.abstract_models import AbstractCity, AbstractRegion, AbstractCountry
from cities_light.receivers import connect_default_signals
import cities_light
from cities_light.settings import ICity
from django.db.models.signals import post_save

PRICES = (('LO', 'Cheap'), ('ME', 'Medium'), ('HI', 'High'))
PACE = (('SL', 'Slow'), ('FA', 'Fast'))
PLANNING = (('STR', 'Strict'), ('REL', 'Relaxed'))
ACTIVITIES = (('SIT', 'Sightseeing'), ('NAT', 'Nature'), ('PAR', 'Partying & Nightlife'), ('MUS', 'Museums'), ('ART', 'Art'), ('FOO', 'Food & Dining'), ('OFF', 'Off the beaten path'), ('ACT', 'Active & Exercise'))

def set_city_fields(sender, instance, items, **kwargs):
    instance.timezone = items[ICity.timezone]

cities_light.signals.city_items_post_import.connect(set_city_fields)

class Country(AbstractCountry):
    pass

connect_default_signals(Country)

class Region(AbstractRegion):
    pass

connect_default_signals(Region)

class City(AbstractCity):
    pass
    timezone = models.CharField(max_length = 40)

connect_default_signals(City)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    age = models.IntegerField(blank = True, null = True)
    home_country = models.ForeignKey(Country, related_name = 'personcountry', blank = True, null = True)
    home_city = models.ForeignKey(City, related_name = 'personcity', blank = True, null = True)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)

class Itinerary(models.Model):
    country = models.ForeignKey(Country, related_name = 'itinerarycountry', blank = True, null = True)
    city = models.ForeignKey(City, related_name = 'itinerarycity', blank = True, null = True)
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.CharField(max_length = 3, choices = PRICES)
    pace = models.CharField(max_length = 2, choices = PACE)
    name = models.CharField(max_length = 100)
    description = models.TextField()
    owner = models.ForeignKey(User, related_name = 'itineraries')
