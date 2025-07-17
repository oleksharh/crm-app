from .api_client import build_calendar_service


def fetch_events_for_token(token, time_min, time_max) -> list[dict]:
    """Fetches events from the user's calendar using the provided access token."""
    service = build_calendar_service(token)

    events_result = service.events().list(
        calendarId='primary',
        timeMin=time_min,
        timeMax=time_max,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    return events_result.get('items', [])
