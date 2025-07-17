# calendar_api/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('calendar/events/', views.fetch_events_for_day, name='fetch-events'),
]
