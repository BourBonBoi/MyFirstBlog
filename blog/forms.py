from django import forms
from .models import *


class AddPostForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ['title', 'slug', 'content', 'photo', 'category']  # Не забудьте добавить поле `category`

        widgets = {
            'content': forms.Textarea(attrs={'rows': 5, 'cols': 40}),
        }
