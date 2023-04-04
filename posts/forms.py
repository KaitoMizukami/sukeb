from django import forms

from .models import Comment, Post, Skatepark
from .prefectures import PREFECTURE_CHOICES


class PostForm(forms.ModelForm):
    """
    投稿用フォーム
    """
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['body'].label = '投稿内容' # labelの文字を変更

    body = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'input mb-5'
        }
    ))

    class Meta:
        model = Post 
        exclude = ['author', 'skatepark']
    
    prefix = 'post'


class SkateparkForm(forms.ModelForm):
    """
    スケートパーク用フォーム
    """
    def __init__(self, *args, **kwargs):
        super(SkateparkForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'スケートパーク名'
        self.fields['prefecture'].label = '都道府県'
        self.fields['city'].label = '市町村'
        self.fields['skatepark_image'].label = '写真'

    name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'input mb-5'
        }
    ))

    prefecture = forms.ChoiceField(
        choices = PREFECTURE_CHOICES,
        widget=forms.Select(
            attrs={
                'class': 'select mb-5'
            }
        ) 
    )

    city = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'input mb-5',
        }
    ))

    skatepark_image = forms.ImageField(widget=forms.FileInput(
        attrs={
            'class': 'mb-5'
        }
    ))

    class Meta:
        model = Skatepark
        fields = ['name', 'prefecture', 'city', 'skatepark_image']

    prefix = 'skatepark'


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