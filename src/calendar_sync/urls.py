# calendar_api/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('calendar/events/', views.list_events, name='list-events'),
]
