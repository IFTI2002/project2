from django.contrib import admin
from .models import Listings, Categories, Watchlist

# Register your models here.
admin.site.register(Listings)
admin.site.register(Categories)
admin.site.register(Watchlist)