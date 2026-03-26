from django.urls import path
from .views import *

urlpatterns = [
    path('login/', AdminLoginView.as_view()),
    path('users/', UserListView.as_view()),
    path("users/<int:id>/", UserDetailView.as_view()),
    path("users/<int:id>/toggle-status/", ToggleUserStatus.as_view()),
    path("users/<int:id>/delete/", DeleteUser.as_view()),
    path("products/", ProductCreateView.as_view()),
    # path("products/list/", ProductListView.as_view()),
    path("products/<int:id>/", ProductUpdateView.as_view()),
    path("products/<int:id>/delete/", ProductDeleteView.as_view()),
    path("orders/", OrderListView.as_view()),
    path("orders/<int:id>/", OrderDetailView.as_view()),
    path("orders/<int:id>/status/", UpdateOrderStatus.as_view()),
    # path("dashboard/revenue/", RevenueView.as_view()),
    path("dashboard/orders-count/", OrderCountView.as_view()),
    path("users/deleted/", DeletedUserListView.as_view()),
    path("users/<int:id>/restore/", RestoreUser.as_view()),
    path("orders/count/", OrderCountView.as_view()),
    path("orders-by-category/",OrdersByCategory.as_view()),
    path("monthly-sales/",MonthlySalesView.as_view())
]
