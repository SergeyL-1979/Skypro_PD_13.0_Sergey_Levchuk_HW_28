# from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext as _


# Create your models here.
class Category(models.Model):
    """ Модель Category(КАТЕГОРИЯ) """
    name = models.CharField(_("Наименование"), max_length=64, unique=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return '{}'.format(self.name)


class Location(models.Model):
    """ Модель местоположения """
    name = models.CharField(_("Местоположение"), max_length=250)
    lat = models.FloatField(_("lat"))
    lng = models.FloatField(_("lng"))

    class Meta:
        verbose_name = "Локация"
        verbose_name_plural = "Локации"

    def __str__(self):
        return self.name

class User(models.Model):
    """ Модель пользователя и автора объявлений """
    STATUS = [
        ("admin", "Администратор"),
        ("moderator", "Модератор"),
        ("member", "Участник"),
    ]
    first_name = models.CharField(_("Имя"), max_length=150)
    last_name = models.CharField(_("Фамилия"), max_length=150)
    # username = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Автор')
    username = models.CharField(_("Никнейм"), max_length=150)
    password = models.CharField(_("password"), max_length=150)
    role = models.CharField(_("Права пользователя"), max_length=15, choices=STATUS, default="member")
    age = models.IntegerField(_("Возраст"))
    # location = models.ManyToManyField(Location, verbose_name='Местоположение')
    location = models.ForeignKey(Location, on_delete=models.CASCADE, verbose_name='Местоположение')

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return "{} {}".format(self.last_name, (self.username, ))


class Announcement(models.Model):
    """ Модель Announcements(Объявления) """
    name = models.CharField(_("Наименование"), max_length=150)
    author = models.ForeignKey(User, on_delete=models.CASCADE, max_length=100, verbose_name='Автор')
    price = models.FloatField(_("Цена"))
    description = models.TextField(_("Описание"))
    image = models.ImageField(_("Добавить фото"), upload_to="images")
    is_published = models.BooleanField(_("is_published"))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')

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
        return self.author.username
