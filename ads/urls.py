from django.urls import path
from ads import views
from .views import (
    AnnouncementListView, AnnouncementsDetailView,
    AnnouncementsCreateView, AnnouncementsUpdateView, LocationListView, CategoryCreateView,
    CategoryListView, CategoryUpdateView, CategoryDetailView, UserListView)

urlpatterns = [
    path('', views.root),
    path('ad/', AnnouncementListView.as_view(), name='announce_list'),
    path('ad/<int:pk>/', AnnouncementsDetailView.as_view(), name='announce_detail'),
    path('ad/update/<int:pk>/', AnnouncementsUpdateView.as_view(), name='announce_update'),
    path('create/', AnnouncementsCreateView.as_view(), name='create_announce'),

    path('cat/', CategoryListView.as_view(), name='category_list'),
    path('cat/create/', CategoryCreateView.as_view(), name='category_create'),
    path('cat/<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),
    path('cat/update/<int:pk>/', CategoryUpdateView.as_view(), name='category_update'),

    path('location/', LocationListView.as_view(), name='location_list'),

    path('users/', UserListView.as_view(), name='users_list'),
]