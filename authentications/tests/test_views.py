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

    def test_authenticated_user_redirect_to_main_page(self):
        """ 
        ログイン済みのユーザーは投稿一覧ページにリダイレクトするテスト
        """
        _ = self.client.post(reverse('authentications:login'), self.credentials)
        response = self.client.get(reverse(self.url_name))
        # リダイレクト(302)が発生したかテスト
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse(self.url_name), follow=True)
        # リダイレクト先のHTMLファイルを確認
        self.assertTemplateNotUsed(response, self.template_name)
        self.assertTemplateUsed(response, 'posts/posts_list.html')


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

    def test_authenticated_user_redirect_to_main_page(self):
        """
        ログイン済みのユーザーは投稿一覧ページにリダイレクトされるテスト
        """
        response = self.client.post(reverse(self.url_name), self.credentials, follow=True)
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse(self.url_name), follow=True)
        self.assertTemplateUsed(response, 'posts/posts_list.html')

    def test_redirect_to_login_page_if_user_not_found(self):
        """ 
        ユーザーが見つからなかったらログインページにリダイレクトするテスト
        """
        response = self.client.post(reverse(self.url_name), {
            'email': 'aaaaa@mail.com', 'password': 'aaaaaaaaa'
        }, follow=True)
        self.assertTemplateUsed(response, self.template_name)


class AuthenticationsLogoutViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='testuser', email='test@mail.com')
        user.set_password('testpassword')
        user.save()

    def setUp(self):
        self.client = Client()
        self.credentials = {
            'email': 'test@mail.com', 'password': 'testpassword'
        }
        self.url_name = 'authentications:logout'

    def test_view_url_exists_at_desired_location(self):
        """
        AuthenticationsLogoutViewが正しいURLにあるかテスト
        """
        response = self.client.get('/accounts/logout/')
        # ログアウトはテンプレートはなくリダイレクト(302)する
        self.assertEqual(response.status_code, 302)

    def test_view_url_accessible_by_name(self):
        """ 
        名前つきURLでアクセスできるかテスト
        """
        response = self.client.get(reverse(self.url_name))
        # ログアウトはテンプレートはなくリダイレクト(302)する
        self.assertEqual(response.status_code, 302)

    def test_view_can_logout(self):
        """ 
        ログアウトできるかテスト
        """
        response = self.client.post(reverse('authentications:login'), self.credentials, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)
        response = self.client.get(reverse('authentications:logout'), follow=True)
        self.assertFalse(response.context['user'].is_authenticated)