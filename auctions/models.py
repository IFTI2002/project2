from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Price(models.Models):
    starting_bid = models.IntegerField()
    current_bid = models.IntegerField()
    bid_count = models.IntergerField()

class Listings(models.Model):
    title = models.CharField(max_length=32)
    description = models.CharField(max_length=256)
    bid = models.IntegerField()
    time = models.DateTimeField(auto_now_add=True, null=True)
    image = models.CharField(max_length=2048, null=True)

    def __str__(self):
        return f"{self.id} {self.title}: ${self.bid} {self.description}"