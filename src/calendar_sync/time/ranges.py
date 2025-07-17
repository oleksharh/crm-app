from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


def get_today_time_range_tz_aware(tz: str) -> tuple[datetime, datetime]:
    user_tz = ZoneInfo(tz)
    min_time = datetime.now(user_tz).replace(hour=0, minute=0, second=0, microsecond=0)
    max_time = min_time + timedelta(days=1)

    return min_time, max_time


def get_today_time_range_tz_aware_iso(tz: str) -> tuple[str, str]:
    min_utc, max_utc = get_today_time_range_tz_aware(tz)
    return min_utc.isoformat(), max_utc.isoformat()
