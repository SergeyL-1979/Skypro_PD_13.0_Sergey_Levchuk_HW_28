import json

from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
# from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import generic

from ads.models import Announcement, Category, Location, User
from avito import settings


def root(request):
    return JsonResponse({"STATUS": "OK!"})


# UserList ====== ГОТОВАЯ МОДЕЛЬ ======
class UserListView(generic.ListView):
    """ Модель отображающая весь список пользователей и вывод на страницу не более 10 """
    model = User

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        # users = User.objects.all()
        self.object_list = self.object_list.prefetch_related('location').order_by("username")
        # ========= ПАГИНАЦИЯ С ПОМОЩЬЮ DJANGO ===============
        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        users = []
        for user in page_obj:
            users.append({
                "id": user.pk,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "username": user.username,
                "password": user.password,
                "role": user.role,
                "age": user.age,
                "location": list(map(str, user.location.all())),
            })

        response = {
            "items": users,
            "num_pages": paginator.num_pages,
            "total": paginator.count,
        }

        return JsonResponse(response, safe=False)


# AnnouncementList ======= ГООТОВАЯ МОДЕЛЬ =======
class AnnouncementListView(generic.ListView):
    """ Модель отображающая весь список объектов и вывод на страницу не более 10 """
    model = Announcement
    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        # announce = Announcement.objects.all()

        self.object_list = self.object_list.select_related('author').order_by("name")
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
                "category": i.category_id
            })

        response = {
            "items": announce,
            "num_pages": paginator.num_pages,
            "total": paginator.count,
        }
        return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False})


# CategoryList ======== ГОТОВАЯ МОДЕЛЬ ========
@method_decorator(csrf_exempt, name='dispatch')
class CategoryListView(generic.ListView):
    """ Модель отображает все объекты """
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()

        response = []
        for category in categories:
            response.append({
                "id": category.pk,
                "name": category.name,
            })
        return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False})


# LocationList ======= ГООТОВАЯ МОДЕЛЬ ========
class LocationListView(generic.ListView):
    """ Модель выводить весь список объектов """
    model = Location

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        loc = Location.objects.all()

        response = []
        for res in loc:
            response.append({
                "name": res.name,
                "lat": res.lat,
                "lng": res.lng,
            })

        return JsonResponse(response, safe=False)


# UserDetail ====== ГОТОВАЯ МОДЕЛЬ ДЕТАЛИЗАЦИИ ==============
class UserDetailView(generic.DetailView):
    """ Отображает детальную информацию об объекте """
    model = User

    def get(self, request, *args, **kwargs):
        users = self.get_object()

        return JsonResponse({
            "first_name": users.first_name,
            "last_name": users.last_name,
            "username": users.username,
            "password": users.password,
            "role": users.role,
            "age": users.age,
            # "location": users.location.name,
            "location": list(map(str, users.location.all())),
        })


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
        })


# CategoryDetail ====== ГОТОВАЯ МОДЕЛЬ ДЕТАЛИЗАЦИИ ==============
class CategoryDetailView(generic.DetailView):
    """ Вывод деталей категории """
    model = Category

    def get(self, request, *args, **kwargs):
        category = self.get_object()

        return JsonResponse({
            "id": category.pk,
            "name": category.name,
        })


# UserCreate ====== МОДЕЛЬ СОЗДАНИЯ =========================
@method_decorator(csrf_exempt, name='dispatch')
class UserCreateView(generic.CreateView):
    model = User
    fields = ["first_name", "last_name", "username", "password", "role", "age", "location", ]

    def post(self, request, *args, **kwargs):
        user_data = json.loads(request.body)

        users = User.objects.create(
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            username=user_data["username"],
            password=user_data["password"],
            role=user_data["role"],
            age=user_data["age"],
            # location=user_data["location"],
        )

        users.save()

        return JsonResponse({
            "id": users.pk,
            "first_name": users.first_name,
            "last_name": users.last_name,
            "username": users.username,
            "password": users.password,
            "role": users.role,
            "age": users.age,
            # "location": user.location,
            "location": list(map(str, users.location.all())),
        })


# AnnouncementCreate ========= МОДЕЛЬ CREATE READY ================
@method_decorator(csrf_exempt, name='dispatch')
class AnnouncementCreateView(generic.CreateView):
    model = Announcement
    fields = ["name", "author", "price", "description", "category", ]

    def post(self, request, is_published=None, *args, **keyword):
        announce_data = json.loads(request.body)
        # self.object = self.get_object()
        # print(self.object, "SELF")
        # self.object.image = request.FILES["image"]

        announce = Announcement.objects.create(
            name=announce_data["name"],
            author=get_object_or_404(User, pk=announce_data['author']),
            price=announce_data["price"],
            description=announce_data["description"],
            is_published=announce_data["is_published"],
            category=get_object_or_404(Category, pk=announce_data["category"]),
            # image=announce_data["image"]
        )

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
        })


# CategoryCreate ========= МОДЕЛЬ CREATE ================
@method_decorator(csrf_exempt, name='dispatch')
class CategoryCreateView(generic.CreateView):
    model = Category
    fields = ["name", ]
    def post(self, request, *args, **kwargs):
        category_data = json.loads(request.body)

        category = Category.objects.create(
            name=category_data["name"],
        )

        return JsonResponse({
            "id": category.pk,
            "name": category.name,
        })


# TODO UserUpdate ==================== МОДЕЛЬ РЕДАКТИРОВАНИЯ =====================




# TODO AnnouncementUpdate ============= МОДЕЛЬ UPDATE ===========================
@method_decorator(csrf_exempt, name='dispatch')
class AnnouncementUpdateView(generic.CreateView):
    model = Announcement
    fields = ["name", "author", "price", "description", "is_published", "category", ]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        announce_data = json.loads(request.body)

        self.object.name = announce_data["name"]
        self.object.author = announce_data["author"]
        self.object.price = announce_data["price"]
        self.object.description = announce_data["description"]
        self.object.is_published = announce_data["is_published"]
        self.object.category = announce_data["category"]

        return JsonResponse({
            "name": self.object.name,
            "author": self.object.author,
            "price": self.object.price,
            "description": self.object.description,
            "is_published": self.object.is_published,
            "category": self.object.category,
        })


# TODO CategoryUpdate =========== МОДЕЛЬ РЕДАКТИРОВАНИЯ КАТЕГОРИИ ===================
@method_decorator(csrf_exempt, name='dispatch')
class CategoryUpdateView(generic.UpdateView):
    model = Category
    fields = ["name", ]

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        category_data = json.loads(request.body)

        self.object.name = category_data["name"]
        self.object.save()

        return JsonResponse({
            "id": self.object.pk,
            "name": self.object.name,
        })


# TODO CategoryDelete =========== МОДЕЛЬ УДАЛЕНИЕ КАТЕГОРИИ ===================
@method_decorator(csrf_exempt, name='dispatch')
class CategoryDeleteView(generic.DeleteView):
    model = Category
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"STATUS": "DELETED"})




# TODO LocationDetail ====== МОДЕЛЬ ДЕТАЛИЗАЦИИ ==============
# class LocationDetailView(generic.DetailView):
#     model = Location
#
#     def get(self, request, *args, **kwargs):
#         super().get(request, *args, **kwargs)
#
#         locations = self.get_object()
#
#         response = []
#         for location in locations:
#             response.append({
#                 "name": location.name,
#                 "lat": location.lat,
#                 "lng": location.lng,
#             })
#
#         return JsonResponse(response, safe=False)
