from django.urls import path

from ads import views

urlpatterns = [
    path('', views.AnnouncementListView.as_view(), name='announce_list'),
    path('<int:pk>/', views.AnnouncementDetailView.as_view(), name='announce_detail'),
    path('create/', views.AnnouncementCreateView.as_view(), name='create_announce'),
    path('<int:pk>/update/', views.AnnouncementUpdateView.as_view(), name='announce_update'),
    path('<int:pk>/upload_image/', views.AnnouncementUpdateImageView.as_view(), name='announce_update_image'),
    path('<int:pk>/delete/', views.AnnouncementDeleteView.as_view(), name='announce_delete'),

]