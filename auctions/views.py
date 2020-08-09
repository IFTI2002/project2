from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listings, Categories, Watchlist

def index(request):

    return render(request, "auctions/index.html", {
        "listings": Listings.objects.all()
    })

@login_required(login_url='login')
def listing(request, list_id):

    if request.method == "POST":

        Listings.objects.filter(pk=list_id).update(bid=request.POST["place_bid"])
        Listings.objects.filter(pk=list_id).update(bidder=request.POST["user_id"])

        HttpResponseRedirect(reverse("listing", args=(list_id,)))

    lists = Listings.objects.get(id=list_id)
    
    return render(request, "auctions/listing.html", {
        "listings": lists,
        "users": User.objects.get(id=lists.creator),
        "bidder": User.objects.get(id=lists.bidder)
    })

def categories(request):
    category = Categories.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": category
    })

def category(request, category_id):
    category = Listings.objects.filter(categories=category_id)
    return render(request, "auctions/category.html", {
        "categories": category
    })

def close(request):

    if request.method == "POST":

        delete = Listings.objects.filter(id=request.POST["listings_id"])

        delete.delete()

        return HttpResponseRedirect(reverse("index"))
        

@login_required(login_url='login')
def watchlist(request):

    if request.method == "POST":
        
        watchlist = Watchlist(
            watchlist = request.POST["listings_id"],
            user = request.POST["user_id"]
        )

        watchlist.save()

        return HttpResponseRedirect(reverse("watchlist"))

    return render(request, "auctions/watchlist.html", {
        "watchlist": Watchlist.objects.filter(user=user_id)
    })

@login_required(login_url='login')
def create(request):

    if request.method == "POST": 

        lists = Listings(
            title=request.POST["title"], 
            bid=request.POST["starting_bid"],
            description=request.POST["description"], 
            image=request.POST["image"],
            creator=request.POST["user_id"],
            bidder=request.POST["user_id"],
            categories=Categories.objects.get(category=request.POST["category"])
            )
            
        lists.save()

        return HttpResponseRedirect(reverse("index"))

    category = Categories.objects.all()
    return render(request, "auctions/create.html", {
        "categories": category
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
