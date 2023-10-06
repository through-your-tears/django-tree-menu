from django.db import models

# Create your models here.


class Menu(models.Model):
    class Meta:
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'

    name = models.CharField(max_length=64, verbose_name='Название')
    slug = models.SlugField(max_length=64, verbose_name='Ссылка')

    def __str__(self):
        return self.name


class Item(models.Model):
    class Meta:
        verbose_name = 'Пункт меню'
        verbose_name_plural = 'Пункт меню'

    name = models.CharField(max_length=64, verbose_name='Название')
    slug = models.SlugField(max_length=64, verbose_name='Ссылка')
    menu = models.ForeignKey(Menu, blank=True, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name
