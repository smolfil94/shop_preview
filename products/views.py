from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count,  Q
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView

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
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-date_added')
        size_id = self.request.GET.get('size')
        category_id = self.request.GET.get('category')
        collection_id = self.request.GET.get('collection')

        if size_id:
            queryset = queryset.filter(sizes__id=size_id)

        if category_id:
            queryset = queryset.filter(categories__id=category_id)

        if collection_id:
            queryset = queryset.filter(collections__id=collection_id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        selected_size = self.request.GET.get('size')
        selected_category = self.request.GET.get('category')
        selected_collection = self.request.GET.get('collection')

        # Query for sizes and categories with their product counts in the current context
        filtered_queryset = self.get_queryset()

        sizes = Size.objects.annotate(
            product_count=Count('product', filter=Q(product__in=filtered_queryset))
        )
        categories = Category.objects.annotate(
            product_count=Count('products', filter=Q(products__in=filtered_queryset))
        )
        collections = Collection.objects.annotate(
            product_count=Count('products', filter=Q(products__in=filtered_queryset))
        )

        context['sizes'] = sizes
        context['categories'] = categories
        context['collections'] = collections
        context['selected_size'] = selected_size
        context['selected_category'] = selected_category
        context['selected_collection'] = selected_collection

        return context



class ProductDetailView(View):
    template_name = 'product-details.html'

    def get(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)
        sizes = product.sizes.all()
        colors = product.colors.all()
        context = {
            'product': product,
            'sizes': sizes,
            'colors': colors,
        }
        return render(request, self.template_name, context)


class IndexView(View):
    template_name = 'index.html'

    def get(self, request):
        categories = Category.objects.filter(name__in=['Футболка','Шорты','Худи', 'Лонгсливы','Свитшоты'])
        print(categories)  # Проверьте вывод в консоли сервера
        return render(request, self.template_name, {'categories': categories})


class AllCategoriesView(ListView):
    model = Category
    template_name = 'all_categories.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.all()


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'category_detail.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Получаем текущую категорию
        category = self.get_object()

        # Добавляем все категории в контекст
        all_categories = Category.objects.all()
        context['all_categories'] = all_categories

        # Добавляем все продукты, связанные с текущей категорией, в контекст
        category_products = Product.objects.filter(categories=category)

        # Пагинация продуктов
        paginator = Paginator(category_products, 12)  # 12 продуктов на странице
        page = self.request.GET.get('page')

        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

        context['category_products'] = products
        context['page_obj'] = products  # Добавляем page_obj в контекст для шаблона

        # Вычисляем количество отображаемых продуктов
        start_index = products.start_index()
        end_index = products.end_index()
        total_count = paginator.count

        context['start_index'] = start_index
        context['end_index'] = end_index
        context['total_count'] = total_count
        return context


class AllCollectionsView(ListView):
    model = Collection
    template_name = 'all_collections.html'
    context_object_name = 'collections'

    def get_queryset(self):
        return Collection.objects.all()


class CollectionDetailView(DetailView):
    model = Collection
    template_name = 'collection_detail.html'
    context_object_name = 'collection'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Получаем текущую категорию
        colection = self.get_object()

        # Добавляем все категории в контекст
        all_collections = Collection.objects.all()
        context['all_collections'] = all_collections

        # Добавляем все продукты, связанные с текущей категорией, в контекст
        collection_products = Product.objects.filter(collections=colection).order_by('id')

        # Пагинация продуктов
        paginator = Paginator(collection_products, 12)  # 12 продуктов на странице
        page = self.request.GET.get('page')

        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

        context['collection_products'] = products
        context['page_obj'] = products  # Добавляем page_obj в контекст для шаблона

        # Вычисляем количество отображаемых продуктов
        start_index = products.start_index()
        end_index = products.end_index()
        total_count = paginator.count

        context['start_index'] = start_index
        context['end_index'] = end_index
        context['total_count'] = total_count
        return context


class AboutView(TemplateView):
    template_name = 'about.html'


class ContactView(TemplateView):
    template_name = 'contact.html'
