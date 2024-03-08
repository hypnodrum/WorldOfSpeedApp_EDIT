from django import forms
from django.db import models
from WorldOfSpeedApp.profiles.custom_validators import validate_picture_format


class CustomURLField(models.URLField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.validators.append(validate_picture_format)


class CustomFormURLField(forms.URLField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.validators.append(validate_picture_format)