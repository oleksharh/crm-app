from allauth.socialaccount.models import SocialToken

from .fetch_events import fetch_events_for_token
from .parser import get_parsed_event_object
from calendar_sync.db.lessons import create_or_update_lesson


def sync_user_calendar_events(token: SocialToken, min_time: str, max_time: str) -> list[dict]:
    """
    Syncs user calendar events by fetching them using the provided token and time range,
    parsing them, and updating the database with the parsed events.

    :param token: The access token for the user's calendar.
    :param min_time: The start time of the range in ISO 8601 format.
    :param max_time: The end time of the range in ISO 8601 format.
    :return: A list of dictionaries containing the status of each event processed.
    """
    user_events = fetch_events_for_token(token, min_time, max_time)

    if not user_events:
        return [{"error": "No events found for the user."}]

    events_data = []
    for event in user_events:
        parsed_event = get_parsed_event_object(event)
        event_added = create_or_update_lesson(parsed_event)
        events_data.append(event_added)

    return events_data
