from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.views.generic import ListView, DetailView

from .models import Category, Color, Collection, Product, Size


class NewArrivalsView(View):
    template_name = 'new_arrivals.html'

    def get(self, request):
        new_products = Product.objects.order_by('-date_added')[:10]

        context = {
            'new_products': new_products  # Передаем список новых продуктов в контекст
        }
        return render(request, self.template_name, context)



class ProductListView(ListView):
    model = Product
    template_name = 'shop/shop.html'
    context_object_name = 'products'
    paginate_by = 10  # Adjust the number of items per page as needed

    def get_queryset(self):
        # This method is simplified without filter handling
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
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
        categories = Category.objects.all()
        print(categories)  # Проверьте вывод в консоли сервера
        return render(request, self.template_name, {'categories': categories})


class CategoryDetailView(DetailView):
    model = Category

