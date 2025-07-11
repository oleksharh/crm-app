from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .services.google_service import connect_to_calendar, connect_to_calendar_for_user
from datetime import datetime, timedelta, timezone
from .services.event_fetcher import list_events_data

@login_required
def list_events(request):
    list_events_data()
    # service = connect_to_calendar_for_user(request)
    #
    # # Get current date in UTC
    # now = datetime.now(timezone.utc)
    #
    # # Calculate start of week (Monday)
    # start_of_week = now - timedelta(days=now.weekday())
    # start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
    #
    # # Calculate end of week (Sunday 23:59:59)
    # end_of_week = start_of_week + timedelta(days=6, hours=23, minutes=59, seconds=59)
    #
    # # Convert to ISO format with 'Z' for UTC timezone
    # time_min = start_of_week.isoformat().replace('+00:00', 'Z')
    # time_max = end_of_week.isoformat().replace('+00:00', 'Z')
    #
    # events_result = service.events().list(
    #     calendarId='primary',
    #     timeMin=time_min,
    #     timeMax=time_max,
    #     singleEvents=True,
    #     orderBy='startTime'
    # ).execute()
    #
    # events = events_result.get('items', [])
    return JsonResponse({'events': "events"})
