from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Comments(models.Model):
    comment = models.CharField(max_length=256)

    def __str__(self):
        return self.comment

class Categories(models.Model):
    category = models.CharField(max_length=32)

    def __str__(self):
        return self.Categories

class Bids(models.Model):
    bids = models.IntegerField()

class Listings(models.Model):
    title = models.CharField(max_length=32)
    description = models.CharField(max_length=256)
    time = models.DateTimeField(auto_now_add=True, null=True)
    image = models.CharField(max_length=2048, null=True)
    bid = models.IntegerField()
    categories = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name="type")
    comment = models.ForeignKey(Comments, on_delete=models.CASCADE, related_name="commentations", null=True, blank=True)

    def __str__(self):
        return f"{self.id} {self.title}: ${self.bid} {self.description}"