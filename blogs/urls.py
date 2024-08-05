from django.urls import path

from .views import BlogDetailView, BlogListView

urlpatterns = [
    path('', BlogListView.as_view(), name='blog'),
    path('blog/<int:blog_id>/', BlogDetailView.as_view(), name='blog-details'),
]