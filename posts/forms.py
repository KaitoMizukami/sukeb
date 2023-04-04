from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    """
    コメント用フォーム
    """
    body = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'input'
        }
    ))

    class Meta:
        model = Comment
        fields = ['body']