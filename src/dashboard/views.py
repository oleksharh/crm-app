from django.shortcuts import render
from rolepermissions.decorators import has_role_decorator

@has_role_decorator('student')
def student_dashboard(request):
    """
    Render the student dashboard.
    """
    return render(request, "dashboard/student_dashboard.html")

@has_role_decorator('teacher')
def teacher_dashboard(request):
    """
    Render the teacher dashboard.
    """
    return render(request, "dashboard/teacher_dashboard.html")

@has_role_decorator('principal')
def principal_dashboard(request):
    """
    Render the principal dashboard.
    """
    return render(request, "dashboard/principal_dashboard.html")
