from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

# Create your models here.

class User(AbstractUser):

    email = models.CharField(max_length=50, unique=True, validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
                message="Enter a valid email. (must contain '@' and '.')",
                code="invalid_registration",
            )
        ])
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)