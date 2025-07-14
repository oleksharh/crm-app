from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .services.event_fetcher import fetch_events_for_day

@login_required
def list_events(request):
    data = fetch_events_for_day(request)

    return JsonResponse(data)
