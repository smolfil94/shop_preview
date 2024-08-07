# Generated by Django 4.2.11 on 2024-08-03 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('header', models.CharField(default='Заголовок по умолчанию', max_length=200, verbose_name='Заголовок')),
                ('text', models.TextField(help_text='Введите текст записи', verbose_name='Текст')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
                ('image', models.ImageField(blank=True, null=True, upload_to='blog/')),
            ],
            options={
                'verbose_name': 'Публикация',
                'verbose_name_plural': 'Публикация',
                'ordering': ['-pub_date'],
            },
        ),
    ]
