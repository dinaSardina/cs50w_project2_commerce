from django.contrib.auth.models import AbstractUser
from django.db import models

from django.core.validators import MinValueValidator
from decimal import Decimal


class User(AbstractUser):
    pass


class Category(models.Model):
    """
    Model representing a listing category
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class AuctionListing(models.Model):
    """
    Model for auction listings.
    User (seller) add listing
    """
    title = models.CharField(max_length=64)
    description = models.TextField()
    img_url = models.URLField('Image', blank=True)
    starting_bid = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    watch = models.ManyToManyField(User, blank=True, related_name="watchlist")
    is_active = models.BooleanField(default=True)
    winner = models.ForeignKey(User, blank=True, on_delete=models.SET_NULL, related_name="win", null=True)
    category = models.ManyToManyField(Category, blank=True, related_name='items')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id}: {self.title} - {self.starting_bid}'


class Bid(models.Model):
    """
    Model reresenting user's bids
    """
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    bid = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f'A bid ${self.bid} from {self.bidder} for {self.listing}'


class Comment(models.Model):
    """
    Comments to auction listings from users
    """
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
