from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, AuctionListing, Comment
from .forms import CreateListingForm, BidForm


def index(request):
    return render(request, "auctions/index.html", {
        'active_listings': AuctionListing.objects.all()
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


def listing_page(request, listing_id):
    """
    View for particular auction listing page
    """

    listing = AuctionListing.objects.get(id=listing_id)
    comments = Comment.objects.filter(listing=listing_id)

    if request.method == "POST":
        if 'new_comment' in request.POST:
            comment = request.POST.get('new_comment')
            new_comment = Comment.objects.create(
                text=comment,
                user=User.objects.get(username=request.user.username),
                listing=listing
            )
            new_comment.save()

        return HttpResponseRedirect(reverse('listing-page', args=[listing_id]))

    return render(request, 'auctions/listing_page.html', {
        'listing': listing,
        # 'bidding_form': BidForm(),
        'comments': comments,

    })


@login_required
def create_listing(request):
    """
    View for create new listing
    """
    if request.method == "POST":
        new_listing = AuctionListing.objects.create(
            title=request.POST['title'],
            description=request.POST['description'],
            img_url=request.POST['img_url'],
            starting_bid=request.POST['starting_bid'],
            seller=User.objects.get(username=request.user.username)
        )

        new_listing.save()

        return HttpResponseRedirect(reverse('index'))

    return render(request, 'auctions/create_listing.html', {
        'form': CreateListingForm(),
    })
