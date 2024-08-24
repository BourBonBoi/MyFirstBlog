from django import template

register = template.Library()

@register.filter
def truncatechars(value, arg):
    """Обрезает строку до указанного количества символов."""
    if isinstance(value, str) and isinstance(arg, int):
        if len(value) > arg:
            return value[:arg] + '...'  # Добавляем троеточие, если текст обрезан
        return value
    return ''
