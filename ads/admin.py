from django.contrib import admin
from ads.models import Announcement, Category, Location, Author

# Register your models here.
@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'lat', 'lng', )

@admin.register(Author)
class MyUserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'username', 'role', 'age', 'location', )
    # order_by = ('username', )
    ordering = ('username', )


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    """ Отображения полей в админке.
    :param ordering - позволяет делать сортировку выбранной колонки
    :param list_per_page - количество объектов на страницу
    :param list_max_show_all - отобразить все объекты не более указанного количества
    """
    list_display = ('name', 'author', 'price', 'image_', 'description', 'category', )
    readonly_fields = ('image_', )
    list_filter = ('name', 'category')
    ordering = ('-price', )
    list_per_page = 5
    list_max_show_all = 50

# admin.site.register(Announcements)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """ Отображает имена категорий в колонке """
    list_display = ('category_name', )
    ordering = ('category_name', )
