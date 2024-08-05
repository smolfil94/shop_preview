from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count,  Q
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView
import re
import random

from .models import Category, Color, Collection, Product, Size
from blogs.models import Blog
from blogs.views import truncate_text


class NewCollectionView(DetailView):
    model = Collection
    template_name = 'new_collection.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        collection = self.object
        products = collection.products.all()[:5]
        context['products'] = products
        print('Context:', context)
        return context


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
        category = product.categories

        similar_products = Product.objects.filter(categories=category).exclude(pk=product_id)

        similar_products = list(similar_products)
        random.shuffle(similar_products)
        similar_products = similar_products[:4]

        context = {
            'product': product,
            'sizes': sizes,
            'colors': colors,
            'same_category_products': similar_products,
        }
        return render(request, self.template_name, context)


class IndexView(View):
    template_name = 'index.html'

    def get(self, request):
        categories = Category.objects.filter(name__in=['Футболка', 'Шорты', 'Худи', 'Лонгсливы', 'Свитшоты'])

        new_arrivals = Product.objects.order_by('-date_added')[:8]

        new_collections = Collection.objects.order_by('-created_date')[:1]

        new_blogs = Blog.objects.order_by('-pub_date')[:3]

        for collection in new_collections:
            match = re.search(r'(.*)\s+(\S+)$', collection.name)
            if match:
                collection.name_part_1, collection.name_part_2 = match.groups()
            else:
                collection.name_part_1, collection.name_part_2 = collection.name, ''

        new_collections_products = Product.objects.filter(collections=new_collections.first())[:5]
        context = {
            'categories': categories,
            'new_arrivals': new_arrivals,
            'new_collections': new_collections,
            'new_collections_products': new_collections_products,
            # 'popular_products': popular_products,
            'new_blogs': new_blogs,
        }
        for new_blog in context['new_blogs']:
            new_blog.truncated_text = truncate_text(new_blog.text, 50)

        return render(request, self.template_name, context)


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

        category = self.get_object()

        all_categories = Category.objects.all().order_by('id')
        context['all_categories'] = all_categories

        category_products = Product.objects.filter(categories=category)

        paginator = Paginator(category_products, 12)
        page = self.request.GET.get('page')

        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

        context['category_products'] = products
        context['page_obj'] = products

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
        return Collection.objects.all().order_by('id')


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
