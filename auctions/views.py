from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import redirect, render
from .models import Bid, Comment, Listing, Tag, User,  Watchlist


def index(request):
    auction_items = Listing.objects.all()
    return render(request, "auctions/index.html", {
        "items": auction_items
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
            return redirect("index")
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return redirect("index")


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

        #Create a watch list for new users
        Watchlist.objects.create(user=user)
        
        return redirect("index")
    else:
        return render(request, "auctions/register.html")


def list_item(request, list_id):
    if list_id > Listing.objects.count():
        return redirect("index")
    
    else:
        return render(request, "auctions/listing.html", {
            "item": Listing.objects.get(pk=list_id)
        })


@login_required(login_url="login")
def watchlist(request):
    watcher_name = request.user.username
    watcher_id = User.objects.get(username=watcher_name)
    
    # In case there is a user that doesn't have a watch list
    try:
        faves = Watchlist.objects.get(user=watcher_id)
    except Watchlist.DoesNotExist:
        faves = None

    return render(request, "auctions/watchlist.html", {
        "faves": faves,
        "id": watcher_id
    })