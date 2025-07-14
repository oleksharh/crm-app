import json
from django.contrib.auth.decorators import login_required
from rolepermissions.decorators import has_role_decorator
from .google_service import fetch_user_calendar_events_by_token
from .utils import get_today_time_range_iso, get_token_for_user, get_parsed_event_object, create_or_update_lesson


@login_required
@has_role_decorator(["teacher", "principal"])  # inside it uses has_role(user, roles: list[str])
def fetch_events_for_day(request) -> dict:
    user = request.user
    token = get_token_for_user(user)

    if not token:
        return {"error": "No calendar token found for the user."}

    min_time, max_time = get_today_time_range_iso()

    user_events = fetch_user_calendar_events_by_token(token, min_time, max_time)

    if not user_events:
        return {"error": "No events found for the user."}

    events_data_status = []
    for event in user_events:
        parsed_event = get_parsed_event_object(event)
        event_added = create_or_update_lesson(parsed_event)
        events_data_status.append(event_added)

    return {"events": events_data_status}
