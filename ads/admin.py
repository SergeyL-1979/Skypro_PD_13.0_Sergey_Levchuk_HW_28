from django.contrib import admin
from ads.models import Announcements, Category

# Register your models here.
@admin.register(Announcements)
class AnnouncementsAdmin(admin.ModelAdmin):
    """ Отображения полей в админке.
    :param ordering - позволяет делать сортировку выбранной колонки
    :param list_per_page - количество объектов на страницу
    :param list_max_show_all - отобразить все объекты не более указанного количества
    """
    list_display = (
        'name',
        'author',
        'price',
        # 'description',
        'address',
    )
    list_filter = ('address', 'author')
    ordering = ('-price', )
    list_per_page = 5
    list_max_show_all = 50

# admin.site.register(Announcements)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """ Отображает имена категорий в колонке """
    list_display = ('category_name', )
    ordering = ('category_name', )
