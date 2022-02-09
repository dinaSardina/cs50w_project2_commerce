from django.contrib import admin

from .models import AbstractUser, AuctionListing

# Register your models here.
admin.site.register(AuctionListing)