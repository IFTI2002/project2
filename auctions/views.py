from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listings, Categories, Watchlist, Comment

# INDEX
def index(request):

    return render(request, "auctions/index.html", {
        "listings": Listings.objects.all() # RETURN ALL ACTIVE LISTINGS
    })

# LISTING PAGE
@login_required(login_url='login')
def listing(request, list_id):

    if request.method == "POST": # IF METHOD IS POST

        Listings.objects.filter(pk=list_id).update(bid=request.POST["place_bid"]) # UPDATEDS THE CURRENT HIGHEST BID
        Listings.objects.filter(pk=list_id).update(bidder=request.POST["user_id"]) # UPDATES THE CURRENT HIGHEST BIDDER/USER

        return HttpResponseRedirect(reverse("listing", args=(list_id,))) # REDIRECT TO LISTINGS WITH ARGS LISTING ID

    lists = Listings.objects.get(id=list_id)
    
    return render(request, "auctions/listing.html", {
        "listings": lists,
        "users": User.objects.get(id=lists.creator), # RETURN CREATOR OF LISTINGS
        "bidder": User.objects.get(id=lists.bidder), # RETURN THE CURRENT HIGHEST BIDDER/USER
        "min": lists.bid + 1, # CURRENT BID AMOUNT PLUS 1 FOR ERROR CHECKING
        "watchlist": Watchlist.objects.filter(watchlist=list_id), 
        "comments": Comment.objects.filter(listing=list_id)
    })

# COMMENTS
def comment(request, list_id):

    if request.method == "POST":

        comment = Comment(
            comment=request.POST["comment"],
            user=request.user,
            listing=list_id
        )

        comment.save()

        return HttpResponseRedirect(reverse("listing", args=(list_id,))) # REDIRECT TO LISTINGS WITH ARGS LISTING ID

# CATEGORIES
def categories(request):
    category = Categories.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": category # RETURNS ALL CATEGORIES
    })

# CATTEGORY
def category(request, category_id):
    category = Listings.objects.filter(categories=category_id)
    return render(request, "auctions/category.html", {
        "categories": category # RETURNS SPECIFIC CATEGORY
    })

# CLOSE LISTING PAGE
def close(request):

    close = Listings.objects.filter(id=request.POST["listings_id"]) #FILTER IF EQUAL TO ID LISTING
    close.delete() # DELETE LISTING

    return HttpResponseRedirect(reverse("index"))

# REMOVE WATCHLIST
def remove(request):

    remove = Watchlist.objects.filter(user=request.user.id, watchlist=request.POST["remove_id"]) # FILTERS USER.ID AND LIST ID
    remove.delete() # DELETE WATCHLIST

    return HttpResponseRedirect(reverse("watchlist")) # REDIRECT TO WATCHLIST

# WATCHLIST
@login_required(login_url='login')
def watchlist(request):

    if request.method == "POST": # IF METHOD IS POST
            
        watchlist = Watchlist(
            watchlist = request.POST["add_id"],
            user = request.user.id
        )

        watchlist.save() # SAVE CREATED WATCHLIST

        return HttpResponseRedirect(reverse("watchlist"))

    return render(request, "auctions/watchlist.html", {
        "watchlist": Watchlist.objects.filter(user=request.user.id),
        "listings": Listings.objects.all()
    })

# CREATEPAGE
@login_required(login_url='login')
def create(request):

    if request.method == "POST": # IF METHOD IS POST

        lists = Listings(
            title=request.POST["title"], 
            bid=request.POST["starting_bid"],
            description=request.POST["description"], 
            image=request.POST["image"],
            creator=request.POST["user_id"],
            bidder=request.POST["user_id"],
            categories=Categories.objects.get(category=request.POST["category"])
            )
            
        lists.save() # SAVE NEWLY CREATED LISTING

        return HttpResponseRedirect(reverse("index")) # REDIRECT TO INDEX

    category = Categories.objects.all()
    return render(request, "auctions/create.html", {
        "categories": category # RETURN ALL CATEGORIES
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
