from django import template

register = template.Library()

@register.filter
def hours_minutes(value):
    if value is None:
        return ""
    try:
        value = int(value)
        hours = value // 60
        minutes = value % 60
        return f"{hours}시간 {minutes}분"
    except (ValueError, TypeError):
        return value
