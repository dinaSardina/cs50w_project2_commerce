from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class AuctionListing(models.Model):
    """
    Model for auction listings.
    User (seller) add listing
    """
    title = models.CharField(max_length=64)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=8, decimal_places=2)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="items")

    def __str__(self):
        return f'{self.id}: {self.title} - {self.starting_bid}'