from django.contrib import admin
from .models import Listings, Categories

# Register your models here.
admin.site.register(Listings)
admin.site.register(Categories)