from django.contrib import admin
from users.models import Location, User


# Register your models here.
@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'lat', 'lng', )


@admin.register(User)
class MyUserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'username', 'role', 'age', )
    ordering = ('username', )
