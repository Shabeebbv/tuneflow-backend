from django.urls import path
from .views import WishlistView, AddToWishlist, RemoveWishlist

urlpatterns = [

    path("wishlist/", WishlistView.as_view()),

    path("wishlist/add/", AddToWishlist.as_view()),

    path("wishlist/remove/", RemoveWishlist.as_view()),

]