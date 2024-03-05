from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db.models import Sum
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic as views
from django.views.generic import DetailView
from django.contrib.auth import views as auth_views, get_user_model, login


class CreateProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ("username", "email", "password",)

        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "nickname"}),
            "email": forms.EmailInput(attrs={"placeholder": "an active e-mail"}),
            "password": forms.PasswordInput(attrs={"placeholder": "desired password"}),
        }

        help_texts = {'username': None, }

    def clean_password(self):
        password = self.cleaned_data.get("password")
        try:
            validate_password(password)
        except ValidationError as e:
            raise forms.ValidationError(str(e))
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data["password"]
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user


class EditProfileForm(forms.ModelForm):
    current_password = forms.CharField(
        label="Current Password",
        widget=forms.PasswordInput(attrs={"placeholder": "Current Password"}),
        required=False  # Allow users to skip entering current password for other changes
    )
    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={"placeholder": "New Password"}),
        required=False
    )
    new_password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm New Password"}),
        required=False
    )

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")

        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "Username"}),
            "email": forms.EmailInput(attrs={"placeholder": "Email"}),
        }

        help_texts = {'username': None, }

    age = forms.IntegerField(
        label="Age",
        required=False,
        min_value=1,
        widget=forms.NumberInput(attrs={"placeholder": "Enter your age"}),
    )

    profile_picture = forms.URLField(
        label="Profile Picture",
        required=False,
        widget=forms.URLInput(attrs={"placeholder": "Profile Picture URL"})
    )

    def clean(self):
        cleaned_data = super().clean()
        current_password = cleaned_data.get("current_password")
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")

        if new_password1 and new_password1 != new_password2:
            raise forms.ValidationError("The two password fields didn't match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        current_password = self.cleaned_data.get("current_password")
        new_password1 = self.cleaned_data.get("new_password1")
        if current_password and new_password1:
            if not user.check_password(current_password):
                raise forms.ValidationError("Invalid current password.")
            user.set_password(new_password1)
        if commit:
            user.save()
            profile_picture = self.cleaned_data.get("profile_picture")
            age = self.cleaned_data.get("age")
            if profile_picture:
                user.profile.profile_picture = profile_picture
            if age:
                user.profile.age = age
            user.profile.save()
        return user


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


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['password'].widget.attrs['placeholder'] = 'Password'


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

    def get_object(self, queryset=None):
        # Get the user object based on the request's user ID
        obj = super().get_object(queryset)
        # Check if the requested user is the same as the currently logged-in user
        if obj != self.request.user:
            raise Http404("You do not have permission to view this profile.")
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object
        total_car_price = user.cars.aggregate(total_sum=Sum('price'))['total_sum']
        total_car_price = total_car_price if total_car_price is not None else 0
        context['total_car_price'] = total_car_price
        return context


class DeleteProfileView(views.DeleteView):
    model = get_user_model()
    template_name = "profiles/profile-delete.html"
    success_url = reverse_lazy("index")

    def get_object(self, queryset=None):
        # Get the logged-in user
        return self.request.user

    def delete(self, request, *args, **kwargs):
        # Get the logged-in user
        user = self.request.user
        # Ensure the user is not staff
        if user.is_staff:
            raise Http404("You cannot delete a staff user.")
        # Delete the user
        user.delete()
        return super().delete(request, *args, **kwargs)
