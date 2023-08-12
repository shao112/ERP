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