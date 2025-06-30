from django.shortcuts import render


def student_dashboard(request):
    """
    Render the student dashboard.
    """
    return render(request, "dashboard/student_dashboard.html")


def teacher_dashboard(request):
    """
    Render the teacher dashboard.
    """
    return render(request, "dashboard/teacher_dashboard.html")


def principal_dashboard(request):
    """
    Render the principal dashboard.
    """
    return render(request, "dashboard/principal_dashboard.html")
