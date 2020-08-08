from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Categories(models.Model):
    category = models.CharField(max_length=32)

    def __str__(self):
        return self.category

class Listings(models.Model):
    title = models.CharField(max_length=32)
    description = models.CharField(max_length=256, null=True)
    time = models.DateTimeField(auto_now_add=True, null=True)
    image = models.CharField(max_length=2048, null=True)
    bid = models.IntegerField()
    categories = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name="type")
    comment = models.CharField(max_length=256, null=True, blank=True)

    def __str__(self):
        return f"{self.id} - {self.title}: ${self.bid} ({self.categories}) {self.time}"