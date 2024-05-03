from django.contrib import admin

from .models import Category, Color, Collection, Product, Size

admin.site.register(Category)
admin.site.register(Color)
admin.site.register(Collection)
admin.site.register(Product)
admin.site.register(Size)
