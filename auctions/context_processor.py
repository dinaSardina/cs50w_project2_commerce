from .models import User


def watchlist_count(request):
    """
    Return count of items in watchlist for authenticated users
    """
    if request.user.is_authenticated:
        user = request.user
        count = user.watchlist.count()
    else:
        count = None
    context = {
        'w_count': count
    }
    return context
