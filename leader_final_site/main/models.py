from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    parent_name = models.CharField()
