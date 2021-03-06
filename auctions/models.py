from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Categories(models.Model):
    category = models.CharField(max_length=32) # CATEGORIES

    def __str__(self):
        return self.category

class Comment(models.Model):
    comment = models.CharField(max_length=256, null=True, blank=True) # COMMENT
    user = models.CharField(max_length=32)
    listing = models.IntegerField()

    def __str__(self):
        return f"id #{self.id} | user #{self.user} | listing #{self.listing}"

class Listings(models.Model):
    title = models.CharField(max_length=32) # TITLE
    description = models.CharField(max_length=256, null=True) # DESCRIPTION
    time = models.DateTimeField(auto_now_add=True, null=True) # DATE AND TIME
    image = models.URLField(max_length=2048, null=True) # IMAGE URL 
    bid = models.IntegerField() # CURRENT BID
    categories = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name="type") # CATEGORIES
    creator = models.CharField(max_length=32) # CREATOR OF THE LISTING
    bidder = models.CharField(max_length=32) # CURRENT HIGHEST BIDDER
    close = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.id} - {self.title}: ${self.bid} ({self.categories}) {self.time}"

class Watchlist(models.Model):
    watchlist = models.IntegerField() # LISTING ID
    user = models.IntegerField() # USER ID

    def __int__(self):
        return self.watchlist