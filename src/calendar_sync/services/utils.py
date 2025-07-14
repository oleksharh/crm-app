import json

from allauth.socialaccount.models import SocialAccount, SocialToken



# FIXME: Improvement: Add select_related("user") in SocialAccount.objects.get(...) to reduce DB hits
#  if accessing user later.
# NOTE:❗Security note: You might want to restrict token access to only active users or filter on roles more
#  defensively (user__is_active=True).

def get_token_for_user(user) -> SocialToken | None:
    """
    Fetches the SocialToken for a given user.
    Returns a SocialToken object or None if not found.
    """
    try:
        social_account = SocialAccount.objects.get(user=user)
        token = SocialToken.objects.get(account=social_account)
        return token
    except (SocialAccount.DoesNotExist, SocialToken.DoesNotExist):
        return None


def get_tokens_by_role(role: str | list[str]) -> list[SocialToken]:
    """
    Fetches all SocialTokens for users with a specific role.
    Returns a list of SocialToken objects.
    """
    if isinstance(role, str):
        role = [role]

    tokens = []
    social_accounts = SocialAccount.objects.filter(user__groups__name__in=role).distinct()

    for account in social_accounts:
        token = SocialToken.objects.filter(account=account).first()
        if token:
            tokens.append(token)

    return tokens


from datetime import datetime, timedelta


# FIXME: ❗Returns timezone-naive strings with a 'Z' suffix (faking UTC).
#  Could lead to bugs when used with real UTC-aware datetimes.

def get_today_time_range_iso() -> tuple[str, str]:
    """
    Returns the start and end of the current day in ISO 8601 format with 'Z' suffix.
    """
    time_min = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    time_max = time_min + timedelta(days=1)
    return time_min.isoformat() + 'Z', time_max.isoformat() + 'Z'







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


from lessons.models import Lesson
from groups.models import StudentGroup


def create_or_update_lesson(event: dict) -> dict | None:
    print(event)
    try:
        lesson = Lesson.objects.get(group__name=event.get('lesson_name', ''), start_utc=event.get('start_utc', ''))
        # TODO: Update lesson if data changed, or not, teacher will manually set status to cancelled,
        #  only completed or scheduled are automatically set
    except Lesson.DoesNotExist:
        try:
            group = StudentGroup.objects.get(name=event.get('lesson_name', ''),
                                            teacher__email=event.get('teacher_email', ''))
            if not group.is_active:
                return {"error": "Group is not active."}
        except StudentGroup.DoesNotExist:
            return {"error": "Group not found for the given lesson name and teacher email."}

        # TODO: add fallback for group to be found by attendee emails only, store them as a fallback entry which does
        #  not yet exist in the database

        lesson = Lesson.objects.create(
            group=group,
            start_utc=event.get('start_utc', ''),
            duration=event.get('duration', 0),
            timezone=event.get('timezone', 'Unknown'),
            status='scheduled',
            notes=f"Created from calendar sync for {event.get('lesson_name', '')}"
        )

    return {"status": "success", "lesson_id": lesson.id, "lesson_name": lesson.name, "start_utc": lesson.start_utc}
