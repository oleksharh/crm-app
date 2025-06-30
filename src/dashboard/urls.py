from django.urls import path
from . import views

urlpatterns = [
    #TODO: these three below should be carriud out of the users app to the core app
#     path("", views.home, name="home"),
#     path("logout", views.logout_view, name="logout"),
#     path("core/", views.core, name="core"),
    path("student/", views.student_dashboard, name="student_dashboard"),
    path("teacher/", views.teacher_dashboard, name="teacher_dashboard"),
    path("principal/", views.principal_dashboard, name="principal_dashboard"),
]