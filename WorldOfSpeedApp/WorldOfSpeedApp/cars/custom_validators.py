from django.core.exceptions import ValidationError


def car_year_validator(year):
    if year < 1950 or year > 2030:
        raise ValidationError("Year must be between 1999 and 2030!")
