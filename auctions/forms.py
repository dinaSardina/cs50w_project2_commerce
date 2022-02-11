from django.forms import ModelForm
from django.core.exceptions import ValidationError

from .models import AuctionListing, Bid


class CreateListingForm(ModelForm):
    class Meta:
        model = AuctionListing
        exclude = ['seller', 'watch']


class NewBidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['bid']
        labels = {'bid': 'Enter your bid'}
