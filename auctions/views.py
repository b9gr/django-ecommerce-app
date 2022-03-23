from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.utils import Error
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import AuctionListings, Bid, Comment, User


def index(request):
    return render(request, "auctions/index.html", {
        "auctions": AuctionListings.objects.all()
    })

def auction(request, auction_id):
    auction = AuctionListings.objects.get(id=auction_id)
    return render(request, "auctions/auction.html", {
        "auction" : auction,
        "offers" : auction.offereds.all(),
        "comments" : auction.listingcomments.all()
    })

@login_required
def makecomment(request, auction_id):
    auction = AuctionListings.objects.get(id=auction_id)
    if request.method == "POST":
        user = request.user
        content = request.POST["comment"]

        new_comment = Comment.objects.create(commenter=user,content=content,commentedListing=auction)
        new_comment.save()

        # check if comment is created
        if new_comment is not None:
            return render(request, "auctions/auction.html", {
                "auction" : auction,
                "comments" : auction.listingcomments.all(),
                "offers" : auction.offereds.all(),
            })
        else:
            return render(request, "auctions/auction.html", {
                "auction" : auction,
                "commentmessage" : "Comment could not be created.",
                "offers" : auction.offereds.all(),
            })

@login_required
def createBid(request, auction_id):
    auction = AuctionListings.objects.get(id=auction_id)
    if request.method == "POST":
        user = request.user
        bid = request.POST["bidoffer"]

        # Check if new offer bigger than current offer
        if float(bid) > auction.bid:
            new_bid = Bid.objects.create(person=user,howmuch=bid,whichListing=auction)
            auction.bid = new_bid.howmuch
            auction.save()
            new_bid.save()
        else:
            return render(request,"auctions/auction.html", {
                "auction" : auction,
                "offers" : auction.offereds.all(),
                "comments" : auction.listingcomments.all(),
                "message" : "Your offer must be bigger than current bid."
            })
        
        # Check if new bid object is created
        if new_bid is not None:
            return render(request,"auctions/auction.html", {
                "auction" : auction,
                "offers" : auction.offereds.all(),
                "comments" : auction.listingcomments.all(),
            })
        else:
            return render(request,"auctions/auction.html", {
                "auction" : auction,
                "offers" : auction.offereds.all(),
                "comments" : auction.listingcomments.all(),
                "message" : "Bid could not be created."
            })


@login_required
def create(request):
    user = request.user
    if request.method == "POST":
        name = request.POST["listingname"]
        bid = request.POST["bid"]
        image = request.POST["filename"]
        category = request.POST["category"]

        # Creating new auction listing
        new_listing = AuctionListings.objects.create(owner=user,name=name,bid=bid,image=image,category=category)
        new_listing.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        # request is not POST
        return render(request, "auctions/create.html", {
            "user" : user
        })

def categories(request):
    categories =  list(set([listing.category for listing in AuctionListings.objects.all()]))
    return render(request, "auctions/categories.html", {
        "categories" : categories
    })

def spesificcategories(request, category):
    # making list of auction listings with specified category among all auction listings
    auctions = [auction for auction in AuctionListings.objects.all() if auction.category == category]
    return render(request, "auctions/spesificcategories.html", {
        "category" : category,
        "auctions" : auctions
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
