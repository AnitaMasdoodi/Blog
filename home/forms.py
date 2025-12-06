from django import forms
from .models import (Category, Post,
                     Comment)

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('image', 'category', 'title', 'text')

class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('image', 'category', 'title', 'text')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']