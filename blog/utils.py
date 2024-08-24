from .models import *


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        categories = Category.objects.all()
        context['categories'] = categories  # Убедитесь, что вы добавляете 'categories'
        return context
