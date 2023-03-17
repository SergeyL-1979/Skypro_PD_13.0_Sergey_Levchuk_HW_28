from django.contrib import admin
from ads.models import Category


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """ Отображает имена категорий в колонке """
    list_display = ('name', )
    ordering = ('name', )
