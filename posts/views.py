from django.shortcuts import render, redirect
from django.views.generic import (
    ListView, DetailView
)
from django.db.models import Q

from .models import Post
from .prefectures import PREFECTURE_CHOICES, PREFECTURE_ID
from .forms import CommentForm


class PostsListView(ListView):
    """
    全ての投稿データを取得し,対応したHTMLに渡す
    """
    template_name = 'posts/posts_list.html'
    model = Post

    def get_queryset(self, **kwargs):
        """ 
        デフォルトでPostモデルの全てのデータをリストで返す
        queryキーワードがある場合はマッチしたPostモデルのデータをリストで返す
        """
        queryset = super().get_queryset(**kwargs)
        # GETリクエストパラメータにqueryがあれば、それでフィルタする
        query_keyword = self.request.GET.get('query')
        if query_keyword:
            # locationモデルのprefectureとquery_keywordが一致するデータをフィルタする
            queryset = Post.objects.filter(
                Q(skatepark__prefecture__contains=query_keyword)
            )
        return queryset

    def get_context_data(self, **kwargs):
        """
        テンプレートに渡すコンテキストにデータを加える
        """
        context = super().get_context_data(**kwargs)
        # 全都道府県のリストをコンテキストに追加
        context['prefectures'] = PREFECTURE_CHOICES
        return context


class PostsDetailView(DetailView):
    """
    投稿の詳細情報をHTMLに渡す
    """
    template_name = 'posts/posts_detail.html'
    model = Post

    def get(self, request, pk):
        """ 
        GETメソッドでリクエストが来たらコメントのフォーム、投稿、全都道府県のタプルを渡す
        スケートパークの県名を取得し、ID番号を取得する。そのID番号を使って天気予報 APIにリクエストを送ると
        その地域の現在の天候が返ってくる
        """
        import requests

        comment_form = CommentForm()
        post = Post.objects.get(id=pk)
        comments = post.comment_set.all
        post_prefecture = post.skatepark.prefecture
        # APIリクエストでパラメーターとして使うID番号を取得
        prefecture_id = PREFECTURE_ID[post_prefecture]
        # 天気予報APIにリクエストを送信
        try:
            res = requests.get(f'https://weather.tsukumijima.net/api/forecast?city={prefecture_id}')
            json_res = res.json()
            # 天候情報を取得
            current_weather = json_res['forecasts'][0]['telop']
        except Exception as err:
            current_weather = 'エラーが起きました'
        prefectures = PREFECTURE_CHOICES
        context = {
            'post': post,
            'comments': comments,
            'comment_form': comment_form,
            'prefectures': prefectures,
            'current_weather': current_weather
        }
        return render(request, 'posts/posts_detail.html', context)

    def post(self, request, *args, **kwargs):
        """
        POSTメソッドでリクエストが来たらコメントの検証をする
        検証成功、失敗どちらも同じ投稿詳細ページを返す
        """
        comment_form = CommentForm(request.POST)
        # 投稿のIDを取得
        post_id = self.kwargs.get('pk')
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            post = Post.objects.get(id=post_id)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('posts:detail', pk=post.id)
        return render(request, 'posts/posts_detail', pk=post_id)