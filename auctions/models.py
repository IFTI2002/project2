from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Categories(models.Model):
    category = models.CharField(max_length=32)

    def __str__(self):
        return f"{self.category}"

class Listings(models.Model):
    title = models.CharField(max_length=32)
    description = models.CharField(max_length=256)
    bid = models.IntegerField()
    category = models.ForeignKey("Categories", on_delete=models.CASCADE, related_name="categ")

    def __str__(self):
        return f"{self.title}: {self.bid}"