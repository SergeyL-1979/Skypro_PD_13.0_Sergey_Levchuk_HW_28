from django.db import models
from django.utils.translation import gettext as _


# Create your models here.
class User(models.Model):
    """ Модель пользователя и автора объявлений """
    STATUS = [
        ("admin", "Администратор"),
        ("moderator", "Модератор"),
        ("member", "Участник"),
    ]
    first_name = models.CharField(_("Имя"), max_length=50)
    last_name = models.CharField(_("Фамилия"), max_length=50, null=True, blank=True)
    username = models.CharField(_("Никнейм"), max_length=50)
    password = models.CharField(_("password"), max_length=150)
    role = models.CharField(_("Права пользователя"), max_length=10, choices=STATUS, default="member")
    age = models.IntegerField(_("Возраст"))
    location = models.ManyToManyField("Location", blank=True, verbose_name='Местоположение')
    # location = models.ForeignKey(Location, on_delete=models.CASCADE, verbose_name='Местоположение')

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        # ordering = ["username"]

    def __str__(self):
        return "{} {}".format(self.last_name, (self.username, ))

class Location(models.Model):
    """ Модель местоположения """
    name = models.CharField(_("Местоположение"), max_length=50)
    lat = models.FloatField(_("lat"), null=True)
    lng = models.FloatField(_("lng"), null=True)
    # lat = models.DecimalField(_("lat"), max_digits=8, decimal_places=8, null=True)
    # lng = models.DecimalField(_("lng"), max_digits=8, decimal_places=8, null=True)

    class Meta:
        verbose_name = "Локация"
        verbose_name_plural = "Локации"

    def __str__(self):
        return self.name