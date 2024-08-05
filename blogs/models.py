from django.db import models

from users.models import User


class Blog(models.Model):
    header = models.CharField('Заголовок', max_length=200)
    text = models.TextField(
        'Текст',
        help_text='Введите текст записи')
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True)
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name="blog")
    image = models.ImageField(
        upload_to='blog/',
        blank=True,
        null=True
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикация'

    def __str__(self):
        text = self.text[:15]
        return f'{text}... Автор: {self.author}. Дата: {self.pub_date}'
