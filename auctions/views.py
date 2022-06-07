from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import redirect, render
from django import forms
from .models import Bid, Comment, Listing, Tag, User, Watchlist

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ["post_title", "description","bid_start", "img", "list_tag"]


def index(request):
    auction_items = Listing.objects.all()
    # how to organize bids? want to show current bid but hard to track/line up
    # when not in same order and multiple bids
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
        item = Listing.objects.get(pk=list_id)
        comments = Comment.objects.filter(listing=list_id)
        bids = Bid.objects.filter(listing=list_id)
        top_bid = bids.last()

        if top_bid is None:
            top_bid = item.bid_start

        user_check = request.user

        if user_check is not None and user_check == item.user:
            canedit = True
        else: 
            canedit = False

        return render(request, "auctions/listing.html", {
            "item": item,
            "bids": bids,
            "top": top_bid,
            "comments": comments,
            "editor": canedit,
        })


@login_required(login_url="login")
def watchlist(request):
    watcher = request.user
    # watcher_name = request.user.username
    # watcher_id = User.objects.get(username=watcher_name)
    
    # In case there is a user that doesn't have a watch list
    try:
        # faves = Watchlist.objects.get(user=watcher_id) 
        faves = Watchlist.objects.get(user=watcher) 
    except Watchlist.DoesNotExist:
        faves = None

    return render(request, "auctions/watchlist.html", {
        "faves": faves
    })


def tags(request, tag_name): 
    # check that there is a tag with that name
    try:
        tag_id = Tag.objects.get(post_tag=tag_name)
    except Tag.DoesNotExist:
        tag_id = None

    #if the tag exists, try to find listings with that tag
    if tag_id:
        try: 
            listings = Listing.objects.filter(list_tag=tag_id)
        except Listing.DoesNotExist:
            listings = None
    else:
        listings = None

    return render(request, "auctions/tags.html", {
        "tag": tag_name,
        "listings": listings,
        "id": tag_id
    })


@login_required(login_url="login")
def edit(request, list_id):
    item = Listing.objects.get(pk=list_id)

    if request.user == item.user:
        #edit button from listing, prepopulated w/listing info
        if request.method =='GET': 
            f = ListingForm(instance=item)

            return render(request, "auctions/edit.html", {
                "form": f,
                "item": item
            })

        #when save button pressed, save listing & redirect to listing    
        elif request.method == 'POST':
            f = ListingForm(request.POST, request.FILES, instance=item)
            
            if f.is_valid():
                f.save()
                return redirect('list_item', list_id)
    
    else:
        return redirect('list_item', list_id)


@login_required(login_url="login")
def new(request):
    if request.method =='GET': 
        f = ListingForm()

        return render(request, "auctions/new.html", {
            "form": f
        })

    #when save button pressed, save listing & redirect to listing    
    elif request.method == 'POST':
        f = ListingForm(request.POST, request.FILES)
        
        if f.is_valid():
            #check for duplicates and make post_title unique in models?
            newlist = f.save(commit=False)
            newlist.user = request.user
            newlist.save()
    
            recent = Listing.objects.count()
            return redirect('list_item', recent)