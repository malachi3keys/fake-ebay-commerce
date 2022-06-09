from queue import Empty
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
        labels = {
            "post_title": "Title",
            "bid_start": "Starting Bid",
            "img": "Image",
            "list_tag": "Tags (Ctrl+Click to select multiple)"
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["body"]
        labels = {
            "body": "",
        }
        widgets = {
            "body": forms.Textarea(attrs={"cols": 100, "rows": 2, "placeholder":"Leave a comment"})
        }

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ["dollar"]
        labels = {
            "dollar": "Make a bid",
        }
        help_texts = {
            "dollar": "(Must be greater than current bid)"
        }
        # error_messages = {
        #     "dollar": {
        #         "invalid":"Bid must be greater than highest bid"
        #         },
        # }


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
    listNum = Listing.objects.count()

    if list_id > listNum:
        return redirect("index")  
    else:
        item = Listing.objects.get(pk=list_id)
        comments = Comment.objects.filter(listing=list_id)
        bids = Bid.objects.filter(listing=list_id)

        if bids:
            top_bid = bids.last().dollar
        else: 
            top_bid = float(item.bid_start)             
        
    if request.method =='GET':
        # check if user is signed in
        user_check = request.user

        if user_check.is_authenticated:
 
            # check user is the same as the listing
            # if same can't bid, but can edit
            # create new comment and bid forms
            if user_check == item.user:
                canedit = True
                cform = CommentForm()
                bform = None
    
            else: 
                canedit = False
                cform = CommentForm()
                bform = BidForm()          

        else:   
            cform = None
            bform = None
            canedit = False
            user_check = None
        
        return render(request, "auctions/listing.html", {
            "item": item,
            "bids": bids,
            "top": top_bid,
            "comments": comments,
            "editor": canedit,
            "cform": cform,
            "bform": bform,
            "user": user_check
        })
   
    # only show comment/bid input if logged in?
    elif request.method =='POST': 
        body = request.POST.get("body")
        dollar = request.POST.get("dollar")

        if body:
            cform = CommentForm(request.POST)
            
            if cform.is_valid():
                newComment = cform.save(commit=False)
                newComment.user = request.user
                newComment.listing = item
                newComment.save() 

        elif dollar:
            bform = BidForm(request.POST) 

            if bform.is_valid():
                if float(dollar) > top_bid: 
                    newBid = bform.save(commit=False)
                    newBid.bidder = request.user
                    newBid.listing = item
                    newBid.save()
                else:
                    bform.add_error("dollar", "Bid must be greater than highest bid")
                    # print(bform.errors)
                    # return render(request, "auctions/listing.html", {
                    #      "message": "Bid must be greater than highest bid",
                    #  })

        return redirect('list_item', list_id)

        
@login_required(login_url="login")
def watchlist(request):
    watcher = request.user
    
    # In case there is a user that doesn't have a watch list
    try: 
        faves = Watchlist.objects.get(user=watcher) 
    except Watchlist.DoesNotExist:
        faves = None

    return render(request, "auctions/watchlist.html", {
        "faves": faves
    })



def alltags(request):
    taglist = Tag.objects.all()

    return render(request, "auctions/alltags.html", {
        "tags": taglist
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

    #when save button pressed, save info & redirect to new listing page    
    elif request.method == 'POST':
        f = ListingForm(request.POST, request.FILES)
        
        if f.is_valid():
            #check for duplicates and make post_title unique in models?
            newList = f.save(commit=False)
            newList.user = request.user
            newList.save()
    
            recent = Listing.objects.count()
            return redirect('list_item', recent)