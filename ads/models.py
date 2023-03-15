from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext as _


# Create your models here.
class Category(models.Model):
    """ Модель Category(КАТЕГОРИЯ) """
    category_name = models.CharField(_("name"), max_length=64, unique=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        # return f"Категория: {self.category_name}"
        return '{}'.format(self.category_name)


class Location(models.Model):
    name = models.CharField(_("name"), max_length=250)
    lat = models.FloatField(_("lat"))
    lng = models.FloatField(_("lng"))

    class Meta:
        verbose_name = "Локация"
        verbose_name_plural = "Локации"


class Author(models.Model):
    STATUS = [
        ("admin", "Администратор"),
        ("moderator", "Модератор"),
        ("member", "Участник"),
    ]
    first_name = models.CharField(_("first_name"), max_length=150)
    last_name = models.CharField(_("last_name"), max_length=150)
    username = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Автор')
    # username = models.CharField(_("username"), max_length=150)
    # password = models.CharField(_("password"), max_length=150)
    role = models.CharField(_("role"), max_length=15, choices=STATUS, default="member")
    age = models.IntegerField(_("age"))
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Announcement(models.Model):
    """ Модель Announcements(Объявления) """
    name = models.CharField(_("name"), max_length=150)
    author = models.ForeignKey(User, on_delete=models.CASCADE, max_length=100)
    price = models.FloatField(_("price"))
    description = models.TextField(_("description"))
    image = models.ImageField(_("image"), upload_to="images")
    is_published = models.BooleanField(_("is_published"))
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def image_(self):
        if self.image:
            from django.utils.safestring import mark_safe
            return mark_safe(u'<a href="{0}" target="_blank"><img src="{0}" width="150"/></a>'.format(self.image.url))
        else:
            return '(Нет изображения)'

    image_.short_description = 'Фото'
    image_.allow_tags = True

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"

    def __str__(self):
        return self.author




