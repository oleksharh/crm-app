from django.shortcuts import render
from rolepermissions.decorators import has_role_decorator


@has_role_decorator("student", redirect_url="home")
def student_dashboard(request):
    return render(request, "dashboard/student_dashboard.html")


@has_role_decorator("teacher", redirect_url="home")
def teacher_dashboard(request):
    return render(request, "dashboard/teacher_dashboard.html")


@has_role_decorator("principal", redirect_url="home")
def principal_dashboard(request):
    return render(request, "dashboard/principal_dashboard.html")
