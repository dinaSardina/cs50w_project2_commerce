from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Max
from decimal import Decimal

from .models import User, AuctionListing, Comment, Bid, Category
from .forms import CreateListingForm, NewBidForm


def index(request):
    return render(request, "auctions/index.html", {
        'active_listings': AuctionListing.objects.filter(is_active=True)
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
    user = request.user
    bids = Bid.objects.filter(listing=listing_id)
    last_bid = bids.last()
    if bids:
        max_bid = bids.aggregate(Max('bid'))['bid__max']
        bid_count = bids.count()
    else:
        max_bid = listing.starting_bid
        bid_count = 0

    context = {
        'listing': listing,
        'comments': comments,
        'wl': listing in user.watchlist.all() if user.is_authenticated else None,
        'max_bid': round(max_bid, 2),
        'bid_count': bid_count,
        'bid_form': NewBidForm(),
        'categories': listing.category.all()
    }

    if request.method == "POST":
        if 'new_comment' in request.POST:
            comment = request.POST.get('new_comment')
            new_comment = Comment.objects.create(
                text=comment,
                user=request.user,
                listing=listing
            )
            new_comment.save()
            return HttpResponseRedirect(reverse('listing-page', args=[listing_id]))

        elif 'bid' in request.POST:
            bid = Decimal(request.POST.get('bid'))
            if bid <= max_bid:
                message = 'Your bid must be greater than current bid!'
                context['error_message'] = message
                context['bid_form'] = NewBidForm(initial={'bid': bid})
                return render(request, 'auctions/listing_page.html', context)

            new_bid = Bid.objects.create(
                bidder=user,
                listing=listing,
                bid=bid
            )
            new_bid.save()
            return HttpResponseRedirect(reverse('listing-page', args=[listing_id]))

    return render(request, 'auctions/listing_page.html', context)


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
            seller=request.user
        )
        new_listing.save()

        categories = request.POST.getlist('category')
        for item in categories:
            new_category = Category.objects.get(id=int(item))
            print(category)
            new_listing.category.add(new_category)

        return HttpResponseRedirect(reverse('index'))

    return render(request, 'auctions/create_listing.html', {
        'form': CreateListingForm(),
    })


def switch_watchlist(request, listing_id):
    user = request.user
    listing = AuctionListing.objects.get(id=listing_id)

    if listing not in user.watchlist.all():
        listing.watch.add(user)
    else:
        user.watchlist.remove(listing)
        user.save()
    return HttpResponseRedirect(reverse('listing-page', args=[listing_id]))


@login_required
def watchlist(request):
    user = User.objects.get(username=request.user.username)
    user_wl = user.watchlist.all()
    return render(request, 'auctions/watchlist.html', {
        'watchlist': user_wl,
    })


@login_required
def close_listing(request, listing_id):
    listing = AuctionListing.objects.get(id=listing_id)
    bids = Bid.objects.filter(listing=listing_id)
    last_bid = bids.last()

    if request.method == "POST":
        if request.POST.get('yes'):
            listing.is_active = False
            listing.winner = last_bid.bidder
            listing.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            return HttpResponseRedirect(reverse('listing-page', args=[listing_id]))
    return render(request, 'auctions/close_listing.html', {
        'listing': listing,
        'last_bid': last_bid,
    })


@login_required
def user_listing(request):
    all_listings = AuctionListing.objects.filter(seller=request.user)
    active_listings = all_listings.filter(is_active=True)
    closed_listings = all_listings.filter(is_active=False)
    return render(request, 'auctions/user_listings.html', {
        'active_listings': active_listings,
        'closed_listings': closed_listings,
    })


def category(request, category_id):
    cur_category = Category.objects.get(id=category_id)
    listings = cur_category.items.all()
    return render(request, 'auctions/category.html', {
        'listings': listings,
        'category': cur_category,
    })

def category_list(request):
    all_categories = Category.objects.all()
    return render(request, 'auctions/category_list.html', {
        'all_categories': all_categories
    })