from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def admin_home(request):
    return render(request, 'admin/home.html')

def doctors_blogs(request):
    return render(request, 'admin/doctors_blogs.html')

def doctors(request):
    return render(request, 'admin/doctors.html')

def patients(request):
    return render(request, 'admin/patients.html')

def specialty(request):
    return render(request, 'admin/specialty.html')

def users(request):
    return render(request, 'admin/users.html')

def login_view(request):
    return render(request, 'admin/login.html')
