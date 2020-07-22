from django.urls import path
from . import views

urlpatterns = [
    path('', views.sign_in),
    path('sign_up', views.sign_up),
    path('login', views.login),
    path('logout', views.logout),
    path('admin', views.admin),
    path('admin/login', views.admin_login),
]