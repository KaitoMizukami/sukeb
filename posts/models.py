from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

from .prefectures import PREFECTURE_CHOICES


User = get_user_model()


class Skatepark(models.Model):
    """
    スケートパークに関するモデル
    """
    name = models.CharField(max_length=50, verbose_name='パーク名')
    prefecture = models.CharField(max_length=4, choices=PREFECTURE_CHOICES, verbose_name='県名')
    city = models.CharField(max_length=10, verbose_name='市名')
    skatepark_image = models.ImageField(upload_to='images/', verbose_name='写真')

    class Meta:
        verbose_name = 'スケートパーク'
        verbose_name_plural = 'スケートパーク'

    def __str__(self):
        return f'{self.name}({self.prefecture})'


class Post(models.Model):
    """ 
    投稿に関するモデル
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='投稿者')
    # オブジェクトが最初に作成されたときに、フィールドを now に自動的に設定
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='投稿日')
    skatepark = models.OneToOneField(Skatepark, on_delete=models.CASCADE, verbose_name='スケートパーク')
    body = models.CharField(max_length=300, verbose_name='内容')

    class Meta:
        verbose_name = '投稿'
        verbose_name_plural = '投稿'

    def __str__(self):
        return self.body[:50]

    def get_absolute_url(self):
        """
        各インスタンスに対応するURLを返す 
        """
        return reverse('posts:detail', kwargs={'pk': self.pk})