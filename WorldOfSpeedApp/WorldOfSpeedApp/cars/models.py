from django.contrib.auth.models import User
from django.db import models
from django import forms
from django.core.validators import MinLengthValidator, MinValueValidator
from WorldOfSpeedApp.cars.custom_validators import car_year_validator
from WorldOfSpeedApp.profiles.models import Profile, CustomURLField


class UniqueURLField(models.URLField):
    def formfield(self, **kwargs):
        defaults = {'widget': forms.URLInput(attrs={'placeholder': 'https://...'})}
        defaults.update(kwargs)
        return super().formfield(**defaults)


class Car(models.Model):

    CarType_Rally = "Rally"
    CarType_OpenWheel = "Open-wheel"
    CarType_Kart = "Kart"
    CarType_Drag = "Drag"
    CarType_Other = "Other"

    CHOICES = (
        (CarType_Rally, CarType_Rally),
        (CarType_OpenWheel, CarType_OpenWheel),
        (CarType_Kart, CarType_Kart),
        (CarType_Drag, CarType_Drag),
        (CarType_Other, CarType_Other),
    )

    car_type = models.CharField(max_length=10, choices=CHOICES, blank=False, null=False)
    car_model = models.CharField(max_length=35, validators=(MinLengthValidator(1),), blank=False, null=False)
    year = models.IntegerField(validators=(car_year_validator,), blank=False, null=False)
    image_url = CustomURLField(
        unique=True, blank=False, null=False,
        error_messages={'unique': "This image URL is already in use! Provide a new one."},
    )
    price = models.IntegerField(validators=(MinValueValidator(1),), null=False, blank=False)
    owner = models.ForeignKey(User, related_name='cars', on_delete=models.CASCADE,)
