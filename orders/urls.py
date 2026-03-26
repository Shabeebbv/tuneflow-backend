from django.urls import path
from .views import CreateOrderView, UserOrdersView

urlpatterns = [

    path("orders/create/", CreateOrderView.as_view()),

    path("orders/", UserOrdersView.as_view()),

]