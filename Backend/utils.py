from datetime import date, timedelta
from .models import Clock

def get_weekdays():
    weekdays = []
    today = date.today()
    current_date = today
    while current_date.weekday() < 5:
        weekdays.append(current_date)
        current_date += timedelta(days=1)
    return weekdays

def get_weekly_clock_data(userid):
    weekdays = get_weekdays()
    weekly_clock_data = []
    for weekday in weekdays:
        clock_records = Clock.objects.filter(created_date=weekday).filter(employee_id=userid).order_by('clock_time')
        check_in = clock_records.first().clock_time.strftime('%H:%M') if clock_records else ''
        check_out = clock_records.last().clock_time.strftime('%H:%M') if clock_records else ''
        daily_data = {
            'day': weekday.strftime('%m/%d'),
            'checkin': check_in,
            'checkout': check_out
        }
        weekly_clock_data.append(daily_data)
    return weekly_clock_data
