from django import forms
from WorldOfSpeedApp.cars.models import Car


class CreateCarForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # if I want to show the username of the owner
        # self.fields['owner'].initial = user.username
        # self.fields['owner'].widget = forms.TextInput(attrs={'readonly': 'readonly'})

    class Meta:
        model = Car
        fields = ("car_type", "car_model", "year", "image_url", "price")
        labels = {
            'car_type': 'Type',
            'car_model': 'Model',
            'year': 'Year',
            'image_url': 'Image URL',
            'price': 'Price',
        }

        widgets = {
            "image_url": forms.URLInput(attrs={"placeholder": "https://..."}),
            # "owner": forms.HiddenInput(),
        }

    def save(self, commit=True):
        car = super().save(commit=False)
        if commit:
            car.save()
        return car
