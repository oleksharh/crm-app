from .google_service import fetch_user_calendar_events
from allauth.socialaccount.models import SocialAccount, SocialToken
from datetime import datetime, timedelta


def get_teacher_tokens():
    """
    Fetches all tokens for users with the 'teacher' role.
    Returns a list of SocialToken objects.
    """
    teacher_tokens = []
    teachers = SocialAccount.objects.filter(user__groups__name__in=['teacher', 'principal']).distinct()
    print(teachers)

    for teacher in teachers:
        print(type(teacher))
        print(teacher)
        token = SocialToken.objects.filter(account=teacher).first()
        if token:
            teacher_tokens.append(token)
        else:
            print(f"No token found for teacher account: {teacher}")

    return teacher_tokens


def list_events_data():
    tokens = get_teacher_tokens()
    for token in tokens:
        time_min = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        time_max = time_min + timedelta(hours=24)
        user_events = fetch_user_calendar_events(token, time_min.isoformat() + 'Z', time_max.isoformat() + 'Z')
        for event in user_events:
            print(event)
            lesson_name = event['summary']
            teacher_email = event['creator']['email']
            # self checks if the user is the the teacher if yes then it is not included in the attendees
            attendee_emails = [attendee['email'] for attendee in event['attendees'] if not attendee.get('self', False)]
            # attendees': [{'email': 'alice.hughes18 @ samplemail.com', 'responseStatus': 'needsAction'}, {'email
            # ': 'testcrm2001.01 @ gmail.com', 'organizer': True, 'self': True, 'responseStatus': 'accepted'},
            print(lesson_name, teacher_email, attendee_emails)


