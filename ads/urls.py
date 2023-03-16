from django.urls import path
from ads import views
# from .views import (
#     AnnouncementListView, AnnouncementsDetailView,
#     AnnouncementsCreateView, AnnouncementsUpdateView, LocationListView, CategoryCreateView,
#     CategoryListView, CategoryUpdateView, CategoryDetailView, UserListView, UserDetailView)
from ads import views

urlpatterns = [
    path('', views.root),
    path('ad/', views.AnnouncementListView.as_view(), name='announce_list'),
    path('ad/<int:pk>/', views.AnnouncementDetailView.as_view(), name='announce_detail'),
    path('ad/update/<int:pk>/', views.AnnouncementUpdateView.as_view(), name='announce_update'),
    path('create/', views.AnnouncementCreateView.as_view(), name='create_announce'),

    path('cat/', views.CategoryListView.as_view(), name='category_list'),
    path('cat/create/', views.CategoryCreateView.as_view(), name='category_create'),
    path('cat/<int:pk>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('cat/update/<int:pk>/', views.CategoryUpdateView.as_view(), name='category_update'),

    path('location/', views.LocationListView.as_view(), name='location_list'),
    path('location/<int:pk>/', views.LocationDetailView.as_view(), name='location_list'),

    path('users/', views.UserListView.as_view(), name='users_list'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='users_detail'),
]