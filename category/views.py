import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import generic

from category.models import Category


# Create your views here.
# CategoryList ======================= ГОТОВАЯ МОДЕЛЬ КАТЕГОРИИ =================================
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


# CategoryDetail =============== ГОТОВАЯ КАТЕГОРИЯ ДЕТАЛИЗАЦИИ ==============
class CategoryDetailView(generic.DetailView):
    """ Вывод деталей категории """
    model = Category

    def get(self, request, *args, **kwargs):
        category = self.get_object()

        return JsonResponse({
            "id": category.pk,
            "name": category.name,
        })


# CategoryCreate ========= МОДЕЛЬ КАТЕГОРИЯ СОЗДАНИЯ ================
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


# CategoryUpdate =========== МОДЕЛЬ РЕДАКТИРОВАНИЯ КАТЕГОРИИ ===================
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


# CategoryDelete =========== МОДЕЛЬ УДАЛЕНИЕ КАТЕГОРИИ ===================
@method_decorator(csrf_exempt, name='dispatch')
class CategoryDeleteView(generic.DeleteView):
    model = Category
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"STATUS": "DELETED"})

# =========================== ЗАВЕРШЕНИЕ МОДЕЛИ КАТЕГОРИИ =============================
