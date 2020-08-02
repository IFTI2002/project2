from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listings, Categories


def index(request):
    return render(request, "auctions/index.html")

@login_required(login_url='login')
def watchlist(request):
    return render(request, "auctions/watchlist.html")

def categories(request):
    categories = Categories.objects.all()
    return render(request, "auctions/categories.html",{
        "categories": categories
    })

@login_required(login_url='login')
def create(request):

    if request.method == "POST":
        
        listing = Listings.objects.get()

        category_id = int(request.POST["category"])
        category = Categories.objects.get(pk=category_id)

        category.Listings.add(listing)

        lists = Listings(title=request.POST["title"], bid=request.POST["starting_bid"],
            description=request.POST["description"])

        lists.save()

        return HttpResponseRedirect(reverse("index"))

    categories = Categories.objects.all()
    return render(request, "auctions/create.html",{
        "categories": categories
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
