import json
from django.utils.dateparse import parse_datetime


# FIXME:     ❗Issue: start_utc and end_utc are returned as strings but used as datetime later
#  (parse_datetime(...) in duration) — this causes inconsistency.
#  ❗Better to return real datetime objects, not strings:
#  'start_utc': parse_datetime(start_utc),
#  ❗Hardcoded "Unknown" for timezone makes later logic fragile — fallback to "UTC" if
#  you expect to compute durations or local times.

def get_parsed_event_object(event: dict) -> dict:
    """
    Parses a Google Calendar event object and returns a simplified dictionary.
    """
    print(json.dumps(event, indent=2))
    lesson_name = event.get('summary', 'No Title')
    start_obj = event.get('start', {})
    start_utc = start_obj.get('dateTime', 'No DateTime')
    end_utc = event.get('end', {}).get('dateTime', 'No DateTime')
    timezone = start_obj.get('timeZone', 'Unknown')
    teacher_email = event.get('creator', {}).get('email', 'No Email')
    attendee_emails = [attendee.get('email', 'No Email') for attendee in event.get('attendees', []) if
                       not attendee.get('self', False)]

    parsed_event = {
        'lesson_name': lesson_name,
        'start_utc': start_utc,
        'timezone': timezone,
        'duration': (
            (parse_datetime(end_utc) - parse_datetime(start_utc))
            if start_utc != 'No DateTime' and end_utc != 'No DateTime'
            else 'Unknown'
        ),
        'teacher_email': teacher_email,
        'attendee_emails': attendee_emails
    }

    return parsed_event