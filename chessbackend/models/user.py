from django.contrib.auth.models import AbstractUser
from django.db import models


# How to get user model in the future!
# from django.contrib.auth import get_user_model
# User = get_user_model()


class User(AbstractUser):
    pass
