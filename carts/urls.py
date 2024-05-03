from django.urls import path
from . import views

urlpatterns = [
    path('cart/', views.CartView.as_view(), name='cart'),
    path('add-to-cart/<int:product_id>/', views.AddToCartView.as_view(), name='add_to_cart'),
    path('remove-from-cart/<int:cart_item_id>/', views.RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('update-cart-item/<int:cart_item_id>/', views.UpdateCartItemView.as_view(), name='update_cart_item'),
]
