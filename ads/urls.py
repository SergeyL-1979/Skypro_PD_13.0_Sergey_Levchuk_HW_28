from django.urls import path
from ads import views
from ads.views import AnnouncementsView, AnnouncementsDetailView, CategoryView, CategoryDetailView

urlpatterns = [
    path('', views.status),
    path('ad/', AnnouncementsView.as_view(), name='announce_list'),
    path('ad/<int:pk>', AnnouncementsDetailView.as_view(), name='announce_detail'),
    path('cat/', CategoryView.as_view(), name='category_list'),
    path('cat/<int:pk>', CategoryDetailView.as_view(), name='category_detail'),
]