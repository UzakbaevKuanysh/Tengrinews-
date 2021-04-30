from django.contrib import admin

from core.models import NewsImage, Category, News, Author


class NewsImageInLine(admin.TabularInline):
    model = NewsImage


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'author', 'timestamp')
    inlines = (NewsImageInLine,)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'role')
