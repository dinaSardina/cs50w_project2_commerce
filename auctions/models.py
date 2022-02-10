from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class User(AbstractUser):
    pass


class AuctionListing(models.Model):
    """
    Model for auction listings.
    User (seller) add listing
    """
    title = models.CharField(max_length=64)
    description = models.TextField()
    img_url = models.URLField('Image', blank=True)
    starting_bid = models.DecimalField(max_digits=8, decimal_places=2)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="items")

    def __str__(self):
        return f'{self.id}: {self.title} - {self.starting_bid}'


class Bids(models.Model):
    """
    Model for user's bids
    """
    value = models.DecimalField(max_digits=6, decimal_places=2)
    # listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="bids")
    # bidder = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'A bid {self.value} for {self.listing}'


class Comment(models.Model):
    """
    Comments to auction listings from users
    """
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)


