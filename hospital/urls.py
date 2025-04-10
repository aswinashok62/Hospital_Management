from django.contrib import admin
from django.urls import path ,include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('', include('doctors.urls')),
    path('', include('patients.urls')),
    path('admin/home/', views.admin_home, name='admin_home'),
    path('admin/doctors_blogs/', views.doctors_blogs, name='doctors_blogs'),
    path('admin/doctors/', views.doctors, name='doctors'),
    path('admin/patients/', views.patients, name='patients'),
    path('admin/specialty/', views.specialty, name='specialty'),
    path('admin/users/', views.users, name='users'),
    path('admin/login/', views.login_view, name='login'),
     
]
