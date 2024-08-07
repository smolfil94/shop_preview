from django.contrib import admin

from .models import Category, Color, Collection, Product, Size

admin.site.register(Category)


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_date')  # Добавьте поле date_created сюда
    fields = ('name', 'description', 'image', 'slug')  # Добавьте поле date_created сюда


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'date_added')
    list_filter = ('categories', 'colors', 'collections')
    search_fields = ('name', 'description')
    filter_horizontal = ('sizes', 'colors')

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)