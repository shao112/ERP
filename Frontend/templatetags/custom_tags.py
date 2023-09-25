from django import template
from datetime import datetime
from datetime import date
from Backend.models import ReferenceTable

register = template.Library()




@register.filter(name='highlight_date')
def highlight_date(date_str):
    try:
        print(date_str)
        
        if date_str == date.today():
            return f'<p style="color: red;">{date_str}</p>'
        else:
            return f'<p>{date_str}</p>'
    except ValueError:
        # 如果日期字符串格式不正确，返回原始字符串
        return date_str
    

@register.filter
def format_with_zeros(value, width):
    return str(value).zfill(width)

@register.filter
def Travel_show(user_location_city, location_city):
    try:
        reference_entry = ReferenceTable.objects.get(
            location_city_business_trip=user_location_city,
            location_city_residence=location_city,
            name="車程津貼"
        )
        return reference_entry.amount
    except ReferenceTable.DoesNotExist:
        return f"找不到{location_city}對{user_location_city}的車程津貼參照表 "



@register.filter
def in_group_T_or_F(user, group):
    is_supervisor = False
    is_in_group = any(group in user_group.name for user_group in user.groups.all())

    return is_in_group

@register.filter
def get_supervisor(user):
    is_supervisor = False
    for group in user.groups.all():
        if group.name == '主管':
            is_supervisor = True
            break

    return is_supervisor



@register.filter(name='render_model_text')
def render_model_text(model_value):
    if model_value == 'project_confirmation':
        return '工程確認單'
    elif model_value == 'job_assign':
        return '工程派任計畫'
    elif model_value == 'project_employee_assign':
        return '工程派工單'
    else:
        return '未知'