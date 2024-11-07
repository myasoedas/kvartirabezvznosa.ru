# blogicum/blog/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView

from .models import Comment, Post


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 5,
                'cols': 40,
                'placeholder': 'Введите ваш комментарий...',
                'class': 'custom-textarea-class',
            }),
        }


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email']  # Добавьте поля, которые вам нужны
