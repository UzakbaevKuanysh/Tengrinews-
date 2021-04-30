from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return f'{self.name}'


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    role = models.CharField(max_length=100, verbose_name="Роль")

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Автор"

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    @receiver(post_save, sender=User)
    def create_author(sender, instance, created, **kwargs):
        if created and instance.is_staff:
            Author.objects.create(user=instance)


class News(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заглавие")
    body = models.TextField(verbose_name="Текст")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    author = models.ForeignKey(Author,
                               on_delete=models.CASCADE,
                               verbose_name="Автор",
                               related_name="news",
                               blank=True,
                               null=True)
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 blank=True,
                                 null=True,
                                 verbose_name="Категория",
                                 related_name="news")

    class Meta:
        verbose_name_plural = "Новости"

    def __str__(self):
        return f'{self.title} {self.category}'


class NewsImage(models.Model):
    src = models.ImageField(upload_to='images/products', verbose_name='Картинка')
    news = models.ForeignKey(News,
                             on_delete=models.CASCADE,
                             verbose_name='Новость',
                             related_name='images',
                             blank=True,
                             null=True)

    class Meta:
        verbose_name_plural = 'Картинки новостей'
