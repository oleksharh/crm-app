from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("logout", views.logout_view),
    path("core/", views.core, name="core"),
]