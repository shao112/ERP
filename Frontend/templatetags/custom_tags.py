from django import template
from datetime import datetime

register = template.Library()

@register.filter(name='highlight_date')
def highlight_date(date_str):
    try:
        date_obj = datetime.strptime(date_str, '%Y%m%d')
        today_date = datetime.now().date()
        
        # 如果日期是今天，则返回带有红色样式的 <p> 元素
        if date_obj.date() == today_date:
            return f'<p style="color: red;">{date_str}</p>'
        else:
            return f'<p>{date_str}</p>'
    except ValueError:
        # 如果日期字符串格式不正确，返回原始字符串
        return date_str
    

@register.filter
def format_with_zeros(value, width):
    return str(value).zfill(width)