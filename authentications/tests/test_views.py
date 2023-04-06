from django.test import TestCase, Client
from django.urls import reverse

from authentications.models import User


class AuthenticationsSignupViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='testuser', email='test@mail.com')
        user.set_password('testpassword')
        user.save()

    def setUp(self):
        self.client = Client()
        self.template_name = 'authentications/authentications_signup.html'
        self.credentials = {
            'email': 'test@mail.com', 'password': 'testpassword'
        }
        self.url_name = 'authentications:signup'

    def test_view_url_exists_at_desired_location(self):
        """ 
        AuthenticationsSignupViewが正しいテンプレートファイルを使っているかテスト
        """
        response = self.client.get('/accounts/signup/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        """ 
        名前つきURLでアクセスできるかテスト
        """
        response = self.client.get(reverse(self.url_name))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """ 
        AuthenticationsSignupViewが正しいテンプレートファイルを使っているかテスト
        """
        response = self.client.get(reverse(self.url_name))
        self.assertTemplateUsed(response, self.template_name)

    def test_view_creates_a_new_user(self):
        """
        AuthenticationsSignupViewがユーザーを作るテスト
        """
        before_count = User.objects.all().count()
        response = self.client.post(reverse(self.url_name), {
            'username': 'testuser1', 'email': 'test1@mail.com',
            'password': 'testpassword', 'confirm_password': 'testpassword'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        after_count = User.objects.all().count()
        self.assertNotEqual(before_count, after_count)

    def test_view_redirect_to_main_page_after_success_signup(self):
        """ 
        ユーザー登録に成功したら投稿一覧ページにリダイレクトするテスト
        """
        response = self.client.post(reverse(self.url_name), {
            'username': 'testuser2', 'email': 'test2@mail.com',
            'password': 'testpassword', 'confirm_password': 'testpassword'
        }, follow=True)
        self.assertTemplateUsed(response, 'posts/posts_list.html')

    def test_view_automatically_login_after_success_signup(self):
        """ 
        ユーザー登録に成功したら自動的にログインするテスト
        """
        response = self.client.post(reverse(self.url_name), {
            'username': 'testuser3', 'email': 'test3@mail.com',
            'password': 'testpassword', 'confirm_password': 'testpassword'
        }, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)

    def test_view_render_signup_page_if_form_is_invalid(self):
        """ 
        フォームの検証が失敗した時登録ページにレンダーするテスト
        """
        response = self.client.post(reverse(self.url_name), {})
        self.assertTemplateUsed(response, self.template_name)


class AuthenticationsLoginViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='testuser', email='test@mail.com')
        user.set_password('testpassword')
        user.save()

    def setUp(self):
        self.client = Client()
        self.template_name = 'authentications/authentications_login.html'
        self.credentials = {
            'email': 'test@mail.com', 'password': 'testpassword'
        }
        self.url_name = 'authentications:login'

    def test_view_url_exists_at_desired_location(self):
        """ 
        AuthenticationsLoginViewが正しいテンプレートファイルを使っているかテスト
        """
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        """ 
        名前つきURLでアクセスできるかテスト
        """
        response = self.client.get(reverse(self.url_name))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """ 
        AuthenticationsLoginViewが正しいテンプレートファイルを使っているかテスト
        """
        response = self.client.get(reverse(self.url_name))
        self.assertTemplateUsed(response, self.template_name)

    def test_view_can_login(self):
        """ 
        ログインできるかテスト
        """
        response = self.client.post(reverse(self.url_name), self.credentials, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)

    def test_redirect_to_login_page_if_user_not_found(self):
        """ 
        ユーザーが見つからなかったらログインページにリダイレクトするテスト
        """
        response = self.client.post(reverse(self.url_name), {
            'email': 'aaaaa@mail.com', 'password': 'aaaaaaaaa'
        }, follow=True)
        self.assertTemplateUsed(response, self.template_name)