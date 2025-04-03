from django import forms
from .models import Comment, SubComment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']


class SubCommentForm(forms.ModelForm):
    class Meta:
        model = SubComment
        fields = ['body']
