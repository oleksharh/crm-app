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
