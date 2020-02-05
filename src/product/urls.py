from django.urls import path
from product.views import (
    HomeView,
    ProductDetailView,
    add_to_cart,
    remove_from_cart,
    search_func,
    Order_Summary,
    remove_single_item_from_cart,
    CheckOutView,
    PaymentView,
    Menu_View,
    Contact_View
)

urlpatterns=[
    path('', HomeView.as_view(), name='home'),
    path('add-to-cart/<slug>/', add_to_cart, name="add-to-cart"),
    path('remove-from-cart/<slug>/', remove_from_cart, name="remove-from-cart"),
     path('remove-item-from-cart/<slug>/', remove_single_item_from_cart, name="remove-item-from-cart"),
    path('product/<slug>/', ProductDetailView.as_view(), name="product"),
    path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),
    path('order_summary/', Order_Summary.as_view(), name="order_summary"),
    path('search_result/', search_func, name="search-result"),
    path('checkout/', CheckOutView.as_view(), name='checkout'),
    path('menu/', Menu_View.as_view(), name='menu-page'),
    path('contact/', Contact_View.as_view(), name='contact-page')
]