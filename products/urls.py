from django.urls import path
from .views import IndexView, ProductDetailView, ProductListView

urlpatterns = [
    path('product', ProductListView.as_view(), name='store'),
    path('product/<int:product_id>/', ProductDetailView.as_view(), name='product_detail'),
    path('', IndexView.as_view(), name='index'),

]
