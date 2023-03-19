import json

from django.core.paginator import Paginator
from django.db.models import Count, Avg, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator

from django.views.decorators.csrf import csrf_exempt

from django.views import generic, View

from users.models import Location, User
from avito import settings


# Create your views here.
# UserList ================= ГОТОВАЯ МОДЕЛЬ ПОЛЬЗОВАТЕЛЯ ==================
class UserListView(generic.ListView):
    """ Модель отображающая весь список пользователей и вывод на страницу не более 10 """
    model = User

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        # user_qs = User.objects.all().order_by("username")

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


# UserDetail ====== ГОТОВАЯ МОДЕЛЬ ДЕТАЛИЗАЦИИ ПОЛЬЗОВАТЕЛЯ ==============
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

class UserAdsDetailView(View):
    def get(self, request):
        user_qs = User.objects.annotate(announce=Count('announcement'), filter=Q(announcement__is_published__exact=True))

        paginator = Paginator(user_qs, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number )

        users = []
        for user in page_obj:
            users.append({
                "id": user.pk,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": user.role,
                "age": user.age,
                "location": list(map(str, user.location.all())),
                "total_ads": user.announce,
            })

        response = {
            "items": users,
            "total": paginator.count,
            "num_page": paginator.num_pages,
            "avg": user_qs.aggregate(avg=Avg('announcement'))['avg']
        }

        return JsonResponse(response, safe=False)



# UserCreate ====== МОДЕЛЬ СОЗДАНИЯ ПОЛЬЗОВАТЕЛЯ =========================
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
            # location=user_data["location"], # как добавить локации из POSTMAN?
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
            "location": list(map(str, users.location.all())),
        })


# UserUpdate ==================== МОДЕЛЬ РЕДАКТИРОВАНИЯ =====================
@method_decorator(csrf_exempt, name='dispatch')
class UserUpdateView(generic.UpdateView):
    model = User
    fields =  ["first_name", "last_name", "username", "password", "role", "age", "location", ]

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        user_data = json.loads(request.body)

        self.object.first_name=user_data["first_name"]
        self.object.last_name=user_data["last_name"]
        self.object.username=user_data["username"]
        self.object.password=user_data["password"]
        self.object.role=user_data["role"]
        self.object.age=user_data["age"]
        self.object.save()

        return JsonResponse({
            "id": self.object.pk,
            "first_name": self.object.first_name,
            "last_name": self.object.last_name,
            "username": self.object.username,
            "password": self.object.password,
            "role": self.object.role,
            "age": self.object.age,
            # "location": user.location,
            "location": list(map(str, self.object.location.all())),
        })


# UserDelete ==================== МОДЕЛЬ УДАЛЕНИЕ =====================
@method_decorator(csrf_exempt, name='dispatch')
class UserDeleteView(generic.DeleteView):
    model = User
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"STATUS": "DELETE"})



# ================== ПОЛЬЗОВАТЕЛЬ ЗАВЕРШЕН =======================================================

# LocationList =============== ГООТОВАЯ МОДЕЛЬ МЕСТОПОЛОЖЕНИЯ =================
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

#  LocationDetail ====== МОДЕЛЬ ДЕТАЛИЗАЦИИ ==============
class LocationDetailView(generic.DetailView):
    model = Location

    def get(self, request, *args, **kwargs):
        # super().get(request, *args, **kwargs)
        location = self.get_object()

        return JsonResponse({
                "name": location.name,
                "lat": location.lat,
                "lng": location.lng,
            })

