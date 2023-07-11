from datetime import date, timedelta
from .models import Clock
from urllib.parse import parse_qs


def get_weekdays():
    weekdays = []
    today = date.today()
    current_date = today - timedelta(days=today.weekday())
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

def convent_dict(data):
    data_str = data.decode('utf-8')
    dict_data = parse_qs(data_str)
    new_dict_data = {}
    for key, value in dict_data.items():
        new_dict_data[key] = value[0]
        match  value[0]:
            case "true":
                new_dict_data[key] = True
            case "false":
                new_dict_data[key] =False
            case "csrfmiddlewaretoken":
                pass
            case _:
                new_dict_data[key] = value[0]
    return new_dict_data