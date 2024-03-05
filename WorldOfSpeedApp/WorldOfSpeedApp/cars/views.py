from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from WorldOfSpeedApp.cars.models import Car
from django.views import generic as views


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


def create_car(request):
    if request.method == 'POST':
        form = CreateCarForm(request.POST, user=request.user)  # Pass the current user to the form
        if form.is_valid():
            car = form.save(commit=False)
            car.owner = request.user  # Set the owner attribute to the current user
            car.save()
            return redirect('catalogue')
    else:
        form = CreateCarForm(user=request.user)  # Pass the current user to the form
    return render(request, "cars/car-create.html", {'form': form})


def catalogue(request):
    owner_id = request.user
    if owner_id.is_authenticated:
        cars = Car.objects.filter(owner_id=request.user).order_by('id')
    return render(request, "cars/catalogue.html", {'cars': cars})


class DetailCarView(LoginRequiredMixin, views.DetailView):
    model = Car
    template_name = "cars/car-details.html"
    context_object_name = 'car'

    def get_queryset(self):
        # Ensure that only the cars belonging to the currently authenticated user are retrieved
        return Car.objects.filter(owner=self.request.user)

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Check if the car belongs to the currently authenticated user
        if obj.owner != self.request.user:
            raise Http404("You do not have permission to view this car.")
        return obj


class EditCarView(views.UpdateView):
    model = Car
    template_name = "cars/car-edit.html"
    fields = ("car_type", "car_model", "year", "image_url", "price")
    success_url = reverse_lazy("catalogue")


class DeleteCarView(views.DeleteView):
    model = Car
    template_name = "cars/car-delete.html"
    success_url = reverse_lazy("catalogue")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        car = self.get_object()
        context['car_type'] = car.car_type
        context['car_model'] = car.car_model
        context['car_year'] = car.year
        context['car_image_url'] = car.image_url
        context['car_price'] = car.price
        return context
