from django.contrib.auth.models import AbstractUser, User
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(
        validators=(MinValueValidator(21),),
        help_text="Age requirement: 21 years and above.",
        null=True,
        blank=True,
    )
    profile_picture = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.user.username
