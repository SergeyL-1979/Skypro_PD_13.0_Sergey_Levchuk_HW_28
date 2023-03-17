from django.urls import path
from ads import views
# from .views import (
#     AnnouncementListView, AnnouncementsDetailView,
#     AnnouncementsCreateView, AnnouncementsUpdateView, LocationListView, CategoryCreateView,
#     CategoryListView, CategoryUpdateView, CategoryDetailView, UserListView, UserDetailView)
from ads import views

urlpatterns = [
    path('', views.AnnouncementListView.as_view(), name='announce_list'),
    path('<int:pk>/', views.AnnouncementDetailView.as_view(), name='announce_detail'),
    path('create/', views.AnnouncementCreateView.as_view(), name='create_announce'),
    path('update/<int:pk>/', views.AnnouncementUpdateView.as_view(), name='announce_update'),
    path('delete/<int:pk>/', views.AnnouncementDeleteView.as_view(), name='announce_delete'),

]