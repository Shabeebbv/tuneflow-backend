from django.urls import path
from .views import (
    CartView,
    AddToCartView,
    RemoveFromCartView,
    UpdateCartView
)

urlpatterns = [

    path("cart/", CartView.as_view()),

    path("cart/add/", AddToCartView.as_view()),

    path("cart/remove/", RemoveFromCartView.as_view()),

    path("cart/update/", UpdateCartView.as_view()),

]