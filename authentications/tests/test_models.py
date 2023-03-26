from django.test import TestCase
from django.db.utils import IntegrityError, DataError

from authentications.models import User


class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='testuser', email='test@mail.com')
        user.set_password('testpassword')
        user.save()
    
    def setUp(self):
        self.user = User.objects.get(id=1)

    def test_email_label(self):
        """
        ラベルをメールアドレスにするテスト
        """
        user = User.objects.get(id=1)
        field_label = user._meta.get_field('email').verbose_name
        self.assertEqual(field_label, 'メールアドレス')
    
    def test_username_label(self):
        """
        ラベルをユーザーネームにするテスト
        """
        user = User.objects.get(id=1)
        field_label = user._meta.get_field('username').verbose_name
        self.assertEqual(field_label, 'ユーザーネーム')

    def test_email_unique(self):
        """ 
        メールアドレスがユニークかテスト
        """
        user = User.objects.get(id=1)
        is_unique = user._meta.get_field('email').unique
        self.assertTrue(is_unique)
    
    def test_email_max_length_250(self):
        """
        メールアドレスを最大250字にするテスト
        """
        user = User.objects.get(id=1)
        max_length = user._meta.get_field('email').max_length
        self.assertEqual(max_length, 250)

    def test_raises_error_when_email_over_250_characters(self):
        """
        メールアドレスが250以上の時エラーをあげるテスト
        """
        user = User(email='a'*242+'@mail.com', password='testuser', username='test')
        with self.assertRaises(DataError):
            user.save()
    
    def test_username_max_length_100(self):
        """
        ユーザーネームを最大100字にするテスト
        """
        user = User.objects.get(id=1)
        max_length = user._meta.get_field('username').max_length
        self.assertTrue(max_length, 100)

    def test_raises_error_when_username_over_100_characters(self):
        """
        ユーザーネームが100字以上の時エラーをあげるテスト
        """
        user = User(username='a'*101, email='test@mail.com', password='testpassword')
        with self.assertRaises(DataError):
            user.save()

    def test_set_is_staff_False_by_default(self):
        """
        is_staffをデフォルトでFalseにするテスト
        """
        self.assertFalse(self.user.is_staff)

    def test_set_is_superuser_False_by_default(self):
        """
        is_superuserをデフォルトでFalseにするテスト
        """
        self.assertFalse(self.user.is_superuser)

    def test_set_is_active_True_by_default(self):
        """
        is_activeをデフォルトでTrueにするテスト
        """
        self.assertTrue(self.user.is_active)

    def test_raise_error_if_email_is_duplicated(self):
        """
        メールアドレスが重複してる時エラーをあげるテスト
        """
        error_user = User(username='testuser', email='test@mail.com', password='testuser')
        with self.assertRaises(IntegrityError):
            error_user.save()

    def test_user_object_as_string_is_equal_to_username(self):
        """ 
        オブジェクト文字列がユーザーネームと一致するテスト
        """
        self.assertEqual(str(self.user), self.user.username)
    
    def test_can_create_a_user(self):
        """ 
        ユーザーを作るテスト
        """
        before_count = User.objects.all().count
        _ = User.objects.create_user(
            email='test1@mail.com', username='test', password='testpassword'
        )
        after_count = User.objects.all().count
        self.assertNotEqual(before_count, after_count)

    def test_raise_error_if_email_is_empty(self):
        """
        メールアドレスが空の時エラーをあげるテスト
        """
        with self.assertRaises(ValueError):
            _ = User.objects.create_user(email='', username='test', password='testpassword')

    def test_raise_error_if_username_is_empty(self):
        """
        ユーザーネームが空の時エラーをあげるテスト
        """
        with self.assertRaises(ValueError):
            _ = User.objects.create_user(email='test@mail.com', username='', password='testpassword')

    def test_email_should_normalize(self):
        """
        メールアドレスのドメイン部分を正規化するテスト
        """
        email = 'test2@MAIL.COM'
        user = User.objects.create_user(
            email='test2@mail.com', username='test', password='testpassword'
        )
        self.assertEqual(user.email, email.lower())

    def test_password_should_be_hashed(self):
        """
        パスワードをハッシュ化するテスト
        """
        password = 'testpassword'
        user = User.objects.create_user(
            email='test3@mail.com', username='test', password=password
        )
        self.assertNotEqual(password, user.password)

    def test_can_create_a_speruser(self):
        """
        スーパーユーザーを作るテスト
        """
        superuser = User.objects.create_superuser(
            email='test4@mail.com', username='test', password='testpassword'
        )
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)