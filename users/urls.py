from django.urls import path

from users import views

urlpatterns = [
    path('', views.UserListView.as_view(), name='users_list'),
    path('<int:pk>/', views.UserDetailView.as_view(), name='users_detail'),
    path('create/', views.UserCreateView.as_view(), name='users_create'),
    path('update/<int:pk>/', views.UserUpdateView.as_view(), name='users_update'),
    path('delete/<int:pk>/', views.UserDeleteView.as_view(), name='users_delete'),

    path('location/', views.LocationListView.as_view(), name='location_list'),
    path('location/<int:pk>/', views.LocationDetailView.as_view(), name='location_detail'),
    # TODO === не выполнено LocationDetailView
    # path('location/<int:pk>/', views.LocationDetailView.as_view(), name='location_list'),

]