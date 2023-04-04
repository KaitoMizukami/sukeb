from django.test import TestCase, Client, RequestFactory
from django.urls import reverse

from posts.models import Skatepark, Post
from posts.views import PostsListView
from posts.prefectures import PREFECTURE_CHOICES
from authentications.models import User


class PostsListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        skatepark1 = Skatepark(name='test1', prefecture='神奈川県', city='横浜市', skatepark_image='test1')
        skatepark1.save()
        skatepark2 = Skatepark(name='test1', prefecture='東京都', city='渋谷', skatepark_image='test2')
        skatepark2.save()
        skatepark3 = Skatepark(name='test2', prefecture='神奈川県', city='横浜市', skatepark_image='test2')
        skatepark3.save()
        post1 = Post(body='This is test1', skatepark=skatepark1)
        post1.author = User.objects.create(username='test1', email='test1@mail.com', password='testpassword')
        post1.save()
        post2 = Post(body='This is test2', skatepark=skatepark2)
        post2.author = User.objects.create(username='test2', email='test2@mail.com', password='testpassword')
        post2.save()

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.user = User.objects.create(username='loginuser', email='loginuser@mail.com', password='testpassword')
        self.url_name = 'posts:list'
        self.template_name = 'posts/posts_list.html'

    def test_view_url_exists_at_desired_location(self):
        """ 
        PostListViewが正しいURLにあるかテスト
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        """ 
        名前つきURLでアクセスできるかテスト
        """
        response = self.client.get(reverse(self.url_name))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """ 
        PostListViewが正しいテンプレートファイルを使っているかテスト
        """
        response = self.client.get(reverse(self.url_name))
        self.assertTemplateUsed(response, self.template_name)

    def test_return_all_posts_if_no_request_params(self):
        """ 
        リクエストパラメーターがない時全ての投稿を返すかテスト
        """
        request = self.factory.get(reverse(self.url_name))
        view = PostsListView()
        view.request = request
        qs = view.get_queryset()
        self.assertQuerysetEqual(qs, Post.objects.all(), ordered=False)

    def test_get_queryset_with_prefecture_query(self):
        """
        リクエストパラメーターをつけると県名が全て同じ投稿になる
        """
        request = self.factory.get(reverse(self.url_name), {'query': '神奈川県'})
        view = PostsListView()
        view.request = request
        posts = view.get_queryset()
        for post in posts:
            self.assertEqual(post.skatepark.prefecture, '神奈川県')

    def test_get_context_data(self):
        """ 
        コンテキストに全ての県データがあるかテスト
        """
        request = self.factory.get(reverse(self.url_name))
        response = PostsListView.as_view()(request)
        self.assertIsInstance(response.context_data, dict)
        self.assertEqual(response.context_data['prefectures'], PREFECTURE_CHOICES)


class PostsCreateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username='loginuser', email='loginuser@mail.com', password='testpassword')
        self.url_name = 'posts:create'
        self.template_name = 'posts/posts_create.html'

    def test_view_url_exists_at_desired_location(self):
        """ 
        PostsCreateViewが正しいURLにあるかテスト
        """
        response = self.client.get('/posts/create/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        """ 
        名前つきURLでアクセスできるかテスト
        """
        response = self.client.get(reverse(self.url_name))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """ 
        PostsCreateViewが正しいテンプレートファイルを使っているかテスト
        """
        response = self.client.get(reverse(self.url_name))
        self.assertTemplateUsed(response, self.template_name)