from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.generic import ListView

from.models import Blog


def truncate_text(text, max_length):
    """Обрезает текст до указанного количества символов и добавляет многоточие."""
    if len(text) > max_length:
        return text[:max_length] + '...'
    return text


class BlogListView(ListView):
    model = Blog
    template_name = 'blog.html'
    context_object_name = 'blogs'
    paginate_by = 10  # Количество объектов на одной странице

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-pub_date')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for blog in context['blogs']:
            # Обрезаем текст блога до 110 символов
            blog.truncated_text = truncate_text(blog.text, 110)
        return context


class BlogDetailView(View):

    template_name = 'blog-details.html'

    def get(self, request, blog_id):
        blog = get_object_or_404(Blog, pk=blog_id)
        context = {
            'blog': blog,
        }
        return render(request, self.template_name, context)
