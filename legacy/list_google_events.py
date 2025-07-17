from legacy.calendar_api import fetch_user_calendar_events_by_token
from calendar_sync.google.tokens import get_tokens_by_role
from calendar_sync.time.ranges import get_today_time_range_tz_aware_iso


def list_events_data() -> dict:
    tokens = get_tokens_by_role(['teacher', 'principal'])  # TODO: make it dynamic (user can choose roles, but that's
    # the project is done and needs polishing)

    for token in tokens:
        min_time, max_time = get_today_time_range_tz_aware_iso(tz="UTC")
        user_events = fetch_user_calendar_events_by_token(token, min_time, max_time)
        print(user_events)
        if not user_events:
            return {"error": "No events found for the user."}

        if not {'summary', 'creator', 'attendees', 'start', 'end'}.issubset(user_events[0].keys()):
            return {"error": "Invalid event data structure. Not all required fields are present., Required fields: "
                             "summary, creator, attendees, start, end"}
        for event in user_events:
            print(event)
            lesson_name = event['summary']
            teacher_email = event['creator']['email']
            # self checks if the user is the teacher if yes then it is not included in the attendees
            attendee_emails = [attendee['email'] for attendee in event['attendees'] if not attendee.get('self', False)]
            # attendees': [{'email': 'alice.hughes18 @ samplemail.com', 'responseStatus': 'needsAction'}, {'email
            # ': 'testcrm2001.01 @ gmail.com', 'organizer': True, 'self': True, 'responseStatus': 'accepted'},
            print(lesson_name, teacher_email, attendee_emails)

    return {"message": "Events fetched successfully. For debugging, check the console."}
