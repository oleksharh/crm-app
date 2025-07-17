from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime
from zoneinfo import ZoneInfo


def get_user_timezone_from_google(token: str) -> str:
    creds = Credentials(token)
    service = build('calendar', 'v3', credentials=creds)

    calendar = service.calendarList().get(calendarId='primary').execute()
    return calendar.get('timeZone', 'UTC')


def to_utc_time(time: datetime) -> datetime:
    """
    Convert a naive datetime to UTC.
    If the datetime is already timezone-aware, it will be converted to UTC.
    """
    if time.tzinfo is None:
        raise ValueError("The provided datetime must be timezone-aware.")

    tz_utc = ZoneInfo("UTC")

    return time.astimezone(tz_utc)


def to_utc_time_iso(time: datetime) -> str:
    """
    Convert a naive datetime to UTC and return it as an ISO 8601 string.
    If the datetime is already timezone-aware, it will be converted to UTC.
    """
    utc_time = to_utc_time(time)
    return utc_time.isoformat()
