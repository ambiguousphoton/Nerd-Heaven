from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('', views.home, name = 'home'),
    path('island/<str:pk>/', views.island, name = 'island'),
    path('create-island/', views.create_island, name = 'create-island'),
    path('update-island/<str:pk>', views.update_island, name = 'update-island'),
    path('delete-island/<str:pk>', views.delete_island, name = 'delete-island')

]                                   
