from django.urls import path
from .views import CategoryDetailView, IndexView, ProductDetailView, ProductListView

urlpatterns = [
    path('category/<slug:slug>/',
         CategoryDetailView.as_view(), name='category_detail'),
    path('product', ProductListView.as_view(), name='store'),
    path('product/<int:product_id>/', ProductDetailView.as_view(), name='product_detail'),
    path('', IndexView.as_view(), name='index'),

]
