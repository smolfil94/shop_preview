from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.views.generic import ListView

from .models import Category, Color, Collection, Product, Size


class NewArrivalsView(View):
    template_name = 'new_arrivals.html'

    def get(self, request):
        new_products = Product.objects.get('-date_added')[:10]
        context = {
            'new_products': new_products
        }
        return render(request, self.template_name, context)


class ProductListView(ListView):
    model = Product
    template_name = 'shop/shop.html'
    context_object_name = 'products'

    def get_queryset(self):
        # Получаем текущий запрос к объектам модели Product
        queryset = super().get_queryset()

        # Получаем параметры фильтрации из GET-запроса
        category_filter = self.request.GET.get('category')
        size_filter = self.request.GET.get('size')
        color_filter = self.request.GET.get('color')
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')

        # Применяем фильтры
        if category_filter:
            queryset = queryset.filter(category__name=category_filter)

        if size_filter:
            queryset = queryset.filter(size__name=size_filter)

        if color_filter:
            queryset = queryset.filter(color__name=color_filter)

        if min_price:
            queryset = queryset.filter(price__gte=min_price)

        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['sizes'] = Size.objects.all()
        context['colors'] = Color.objects.all()
        context['selected_category'] = self.request.GET.get('category')
        context['selected_size'] = self.request.GET.get('size')
        context['selected_color'] = self.request.GET.get('color')
        context['selected_min_price'] = self.request.GET.get('min_price')
        context['selected_max_price'] = self.request.GET.get('max_price')
        return context


class ProductDetailView(View):
    template_name = 'product-details.html'

    def get(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)
        context = {
            'product': product
        }
        return render(request, self.template_name, context)


class IndexView(View):
    template_name = 'index.html'

    def get(self, request):
        return render(request, self.template_name)
