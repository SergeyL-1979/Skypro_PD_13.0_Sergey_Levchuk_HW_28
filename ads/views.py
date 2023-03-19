import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator

from django.views.decorators.csrf import csrf_exempt

from django.views import generic

from ads.models import Announcement, User, Category
from avito import settings


def root(request):
    return JsonResponse({"STATUS": "OK!"})


# AnnouncementList ================= ГОТОВАЯ МОДЕЛЬ ОБЪЯВЛЕНИЯ ========================
class AnnouncementListView(generic.ListView):
    """ Модель отображающая весь список объектов и вывод на страницу не более 10 """
    model = Announcement
    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        # announce = Announcement.objects.all()

        self.object_list = self.object_list.select_related('author').order_by("-price")
        # ========= ПАГИНАЦИЯ С ПОМОЩЬЮ DJANGO ===============
        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        announce = []
        for i in page_obj:
            announce.append({
                "id": i.pk,
                "name": i.name,
                "author": i.author.username,
                "price": i.price,
                "description": i.description,
                "category": i.category_id,
                "location": list(map(str, i.author.location.all())),

            })

        response = {
            "items": announce,
            "num_pages": paginator.num_pages,
            "total": paginator.count,
        }
        return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False})


# AnnouncementDetail ====== ГОТОВАЯ МОДЕЛЬ ДЕТАЛИЗАЦИИ ==============
class AnnouncementDetailView(generic.DetailView):
    """ Вывод детальной информации одной карточки объявления """
    model = Announcement

    def get(self, request, *args, **kwargs):
        announce = self.get_object()

        return JsonResponse({
            "id": announce.pk,
            "name": announce.name,
            "author": announce.author.username,
            "price": announce.price,
            "description": announce.description,
            "is_published": announce.is_published,
            "category": announce.category.name,
            "image": announce.image.url if announce.image else None,
            "location": list(map(str, announce.author.location.all())),
        })


# AnnouncementCreate ========= МОДЕЛЬ CREATE READY ================
@method_decorator(csrf_exempt, name='dispatch')
class AnnouncementCreateView(generic.CreateView):
    model = Announcement
    fields = ["name", "author", "price", "description", "category", "image"]

    def post(self, request, is_published=None, *args, **keyword):
        # super().post(request, **keyword)
        announce_data = json.loads(request.body)
        # self.object = self.get_object()
        # print(self.object, "SELF")

        announce = Announcement.objects.create(
            name=announce_data["name"],
            author=get_object_or_404(User, pk=announce_data['author']),
            price=announce_data["price"],
            description=announce_data["description"],
            is_published=announce_data["is_published"],
            category=get_object_or_404(Category, pk=announce_data["category"]),
            # image=announce_data["image"]
        )
        # self.object.image = request.FILES["image"] # как сделать при создании добавить фото?
        # self.object.save()

        return JsonResponse({
            "id": announce.pk,
            "name": announce.name,
            "author_id": announce.author.id,
            "author": announce.author.username,
            "price": announce.price,
            "description": announce.description,
            "is_published": announce.is_published,
            "image": announce.image.url if announce.image else None,
            "category_id": announce.category.pk,
            "category": announce.category.name,
        })

# AnnouncementUpdateImage ================ ОБНОВИТЬ ФОТО ОБЪЯВЛЕНИЯ ====================
@method_decorator(csrf_exempt, name='dispatch')
class AnnouncementUpdateImageView(generic.UpdateView):
    """ Дополнительная модель на добавление/изменение фото в объявлении"""
    model = Announcement
    fields = ["name", "image"]

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        self.object.image = request.FILES["image"]
        self.object.save()

        return JsonResponse({
            "id": self.object.pk,
            "name": self.object.name,
            "author_id": self.object.author.id,
            "author": self.object.author.first_name,
            "price": self.object.price,
            "description": self.object.description,
            "is_published": self.object.is_published,
            "category_id": self.object.category.pk,
            "category": self.object.category.name,
            "image": self.object.image.url if self.object.image else None,
        })


# AnnouncementUpdate ============= МОДЕЛЬ РЕДАКТИРОВАНИЯ ОБЪЯВЛЕНИЯ ===========================
@method_decorator(csrf_exempt, name='dispatch')
class AnnouncementUpdateView(generic.CreateView):
    model = Announcement
    fields = ["name", "author", "price", "description", "is_published", "category", "image"]

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        self.object = self.get_object()

        announce_data = json.loads(request.body)

        self.object.name = announce_data["name"]
        self.object.author = get_object_or_404(User, pk=announce_data["author"])
        self.object.price = announce_data["price"]
        self.object.description = announce_data["description"]
        self.object.category = get_object_or_404(Category, pk=announce_data["category"])
        self.object.save()

        return JsonResponse({
            "id": self.object.pk,
            "name": self.object.name,
            "author_id": self.object.author.id,
            "author": self.object.author.first_name,
            "price": self.object.price,
            "description": self.object.description,
            "is_published": self.object.is_published,
            "category_id": self.object.category.pk,
            "category": self.object.category.name,
            "image": self.object.image.url if self.object.image else None,
        })


# AnnouncementDelete ============= МОДЕЛЬ УДАЛЕНИЕ ОБЪЯВЛЕНИЯ ===========================
@method_decorator(csrf_exempt, name='dispatch')
class AnnouncementDeleteView(generic.DeleteView):
    model = Announcement
    success_url = 'ads/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"STATUS": "DELETE"})

# ============================ ЗАВЕРШЕНА МОДЕЛЬ ОБЪЯВЛЕНИЯ ===========================================



