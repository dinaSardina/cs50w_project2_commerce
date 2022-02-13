from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("auctions/<int:listing_id>", views.listing_page, name='listing-page'),
    path("auctions/create", views.create_listing, name='create-listing'),
    path("auctions/<int:listing_id>/switch_watchlist", views.switch_watchlist, name="switch-w"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("auctions/<int:listing_id>/close", views.close_listing, name='close'),
    path("auctions/my", views.user_listing, name="user-listings"),
]
