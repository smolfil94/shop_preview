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

    class Meta:
        verbose_name = 'Размер'
        verbose_name_plural = 'Размеры'

    def __str__(self):
        return self.name

    @property
    def products(self):
        return Product.objects.filter(sizes=self)


class Color(models.Model):
    name = models.CharField(max_length=100, unique=True)
    name_ru = models.CharField(max_length=100, null=True)
    hex_code = models.CharField(max_length=7)

    class Meta:
        verbose_name = 'Цвет'
        verbose_name_plural = 'Цвета'
    def __str__(self):
        return self.name


class Collection(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(null=True, blank=True)
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

    def get_image_url(self):
        if self.image:
            return self.image.url
        return None

    class Meta:
        verbose_name = 'Коллекция'
        verbose_name_plural = 'Коллекции'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    old_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    date_added = models.DateField(auto_now=True)
    image = models.ImageField(
        upload_to='products/',
        blank=True,
        null=True
    )
    large_image = models.ImageField(
        upload_to='products/large/',
        blank=True,
        null=True
    )
    sizes = models.ManyToManyField(Size, blank=True)
    colors = models.ManyToManyField(Color, blank=True)
    collections = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name='products', null=True, blank=True)
    categories = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', null=True, blank=True)

    def get_image_url(self):
        """Возвращает полный URL для изображения продукта, если оно есть, иначе None."""
        if self.image:
            return self.image.url
        return None

    def get_large_image_url(self):
        """Возвращает полный URL для большого изображения продукта, если оно есть, иначе None."""
        if self.large_image:
            return self.large_image.url
        return None

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name
