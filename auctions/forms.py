from django.forms import ModelForm

from .models import AuctionListing


class CreateListingForm(ModelForm):
    class Meta:
        model = AuctionListing
        exclude = ['seller', 'watch']
