from django.contrib import admin
from ads.models import Announcement


# Register your models here.
@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    """ Отображения полей в админке.
    :param ordering - позволяет делать сортировку выбранной колонки
    :param list_per_page - количество объектов на страницу
    :param list_max_show_all - отобразить все объекты не более указанного количества
    """
    list_display = ('name', 'author', 'price', 'image_', 'category', 'is_published', )
    readonly_fields = ('image_', )
    raw_username_fields = ('author', )
    list_filter = ('category', )
    ordering = ('-price', )
    list_per_page = 5
    list_max_show_all = 50
