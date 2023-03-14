from django.db import models
from django.utils.translation import gettext as _


# Create your models here.
class Announcements(models.Model):
    """ Модель Announcements(Объявления) """
    name = models.CharField(_("name"), max_length=150)
    author = models.CharField(_("author"), max_length=100)
    price = models.FloatField(_("price"))
    description = models.TextField(_("description"))
    address = models.TextField(_("address"))
    is_published = models.BooleanField(_("is_published"))

    def __str__(self):
        return self.author


class Category(models.Model):
    """ Модель Category(КАТЕГОРИЯ) """
    category_name = models.CharField(_("name"), max_length=64, unique=True)

    def __str__(self):
        # return f"Категория: {self.category_name}"
        return '{}'.format(self.category_name)

