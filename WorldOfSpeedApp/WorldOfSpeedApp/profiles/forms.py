from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from WorldOfSpeedApp.profiles.mixin import CustomFormURLField


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

    age = forms.IntegerField(
        label="Age",
        required=False,
        min_value=1,
        widget=forms.NumberInput(attrs={"placeholder": "Enter your age"}),
    )

    profile_picture = CustomFormURLField(
        label="Profile Picture",
        required=False,
        widget=forms.URLInput(attrs={"placeholder": "Profile Picture URL"})
    )

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email",)

        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "Username"}),
            "email": forms.EmailInput(attrs={"placeholder": "Email"}),
        }

        help_texts = {'username': None, }

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


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['password'].widget.attrs['placeholder'] = 'Password'
