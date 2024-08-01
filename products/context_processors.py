from .models import Category, Collection


def categories_processor(request):
    return {
        'categories': Category.objects.all()
    }


def collections_processor(request):
    return {
        'collections': Collection.objects.all()
    }
