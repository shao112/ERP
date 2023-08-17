from django import template
from datetime import datetime
from datetime import date


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