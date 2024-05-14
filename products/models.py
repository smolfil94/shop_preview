from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    image = models.ImageField(
        upload_to='products/',
        blank=True,
        null=True
    )
    slug = models.SlugField(
        'Ключ',
        max_length=100,
        null=False,
        unique=True
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def get_image_url(self):
        if self.image:
            return self.image.url
        return None

    def __str__(self):
        return self.name


class Size(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=100, unique=True)
    hex_code = models.CharField(max_length=7)

    def __str__(self):
        return self.name


class Collection(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    date_added = models.DateField(auto_now=True)
    image = models.ImageField(
        upload_to='products/',
        blank=True,
        null=True
    )
    size = models.ForeignKey(Size, on_delete=models.CASCADE, null=True, blank=True)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, null=True, blank=True)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, null=True, blank=True)
    categories = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)

    def get_image_url(self):
        """Возвращает полный URL для изображения продукта, если оно есть, иначе None."""
        if self.image:
            return self.image.url
        return None

    def __str__(self):
        return self.name
