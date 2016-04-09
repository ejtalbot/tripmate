from django.contrib.auth.models import User
from .models import UserProfile, City, Itinerary
from django import forms

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('age', 'home_country', 'home_city')

class ItineraryForm(forms.ModelForm):
    class Meta:
        model = Itinerary
        fields = ('country', 'city', 'start_date', 'end_date', 'price', 'pace', 'name', 'description')
