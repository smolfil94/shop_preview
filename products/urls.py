from django.urls import path
from .views import (AllCategoriesView, AllCollectionsView, CategoryDetailView, CollectionDetailView,
                    IndexView, ProductDetailView, ProductListView, AboutView, ContactView, NewCollectionView)

urlpatterns = [
    path('about', AboutView.as_view(), name='about'),
    path('contact', ContactView.as_view(), name='contact'),
    path('all-collections/', AllCollectionsView.as_view(), name='all_collections'),
    path('collection/<slug:slug>/',
         CollectionDetailView.as_view(), name='collection_detail'),
    path('all-categories/', AllCategoriesView.as_view(), name='all_categories'),
    path('category/<slug:slug>/',
         CategoryDetailView.as_view(), name='category_detail'),
    path('product', ProductListView.as_view(), name='store'),
    path('product/<int:product_id>/', ProductDetailView.as_view(), name='product_detail'),
    path('', IndexView.as_view(), name='index'),

]
