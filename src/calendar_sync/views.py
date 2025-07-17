from allauth.socialaccount.models import SocialToken
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from rolepermissions.decorators import has_role_decorator
from .google.sync import sync_user_calendar_events
from .google.tokens import get_token_for_user
from .time.ranges import get_today_time_range_tz_aware_iso


@login_required
@has_role_decorator(["teacher", "principal"])
def fetch_events_for_day(request):
    user = request.user

    try:
        token = get_token_for_user(user)
    except SocialToken.DoesNotExist:
        return JsonResponse({"error": "Social account not found."}, status=404)

    try:
        user_tz = user.tz_profile.timezone
    except AttributeError:
        return JsonResponse({"error": "User timezone not set."}, status=400)

    min_time, max_time = get_today_time_range_tz_aware_iso(user_tz)
    user_events = sync_user_calendar_events(token, min_time, max_time)

    return JsonResponse({"events": user_events})
