from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic as views
from django.views.generic import DetailView
from django.contrib.auth import views as auth_views, get_user_model, login
from WorldOfSpeedApp.profiles.forms import CreateProfileForm, EditProfileForm, CustomAuthenticationForm


def get_object_or_404(obj, request_user):
    # Check if the requested object is the same as the currently logged-in user
    if obj != request_user:
        raise Http404("You do not have permission to view this profile.")
    return obj


def create_profile(request):
    if request.method == 'POST':
        form = CreateProfileForm(request.POST)
        if form.is_valid():
            form.save()
            # Log the user in after sign up
            login(request, form.instance)
            return redirect('index')
    else:
        form = CreateProfileForm()
    return render(request, "profiles/profile-create.html", {'form': form})


def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = EditProfileForm(instance=user)
    return render(request, "profiles/profile-edit.html", {'form': form})


class LoginUserView(auth_views.LoginView):
    authentication_form = CustomAuthenticationForm

    def get_success_url(self):
        return reverse_lazy('index')


class LogoutUserView(auth_views.LogoutView):
    def get_success_url(self):
        return reverse_lazy('index')


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = 'profiles/profile-details.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(self.object, self.request.user)
        total_car_price = user.cars.aggregate(total_sum=Sum('price'))['total_sum']
        total_car_price = total_car_price if total_car_price is not None else 0
        context['total_car_price'] = total_car_price
        return context


class DeleteProfileView(views.DeleteView):
    model = get_user_model()
    template_name = "profiles/profile-delete.html"
    success_url = reverse_lazy("index")

    def get_object(self, queryset=None):
        # Get the user object based on the request's user ID
        obj = super().get_object(queryset)
        # Use get_object_or_404 for permission checking
        obj = get_object_or_404(obj, self.request.user)
        return obj

    def delete(self, request, *args, **kwargs):
        if self.request.user.is_staff:
            raise Http404("You cannot delete a staff user.")
        return super().delete(request, *args, **kwargs)
