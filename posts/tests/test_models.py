from django.test import TestCase
from django.db.utils import DataError

from authentications.models import User
from posts.models import Skatepark, Post


class SkateparkModelTest(TestCase):
    def setUp(self):
        self.skatepark = Skatepark(name='Test skatepark', prefecture='神奈川', city='横浜', skatepark_image='test_image.jpg')
        self.skatepark.save()
        self.user = User.objects.create(username='testuser', email='test@mail.com', password='testpassword')
        self.user.save()
    
    def test_name_label(self):
        """
        ラベルをパーク名にするテスト
        """
        field_label = self.skatepark._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'パーク名')
    
    def test_prefecture_label(self):
        """
        ラベルをパーク名にするテスト
        """
        field_label = self.skatepark._meta.get_field('prefecture').verbose_name
        self.assertEqual(field_label, '県名')
    
    def test_city_label(self):
        """
        ラベルをパーク名にするテスト
        """
        field_label = self.skatepark._meta.get_field('city').verbose_name
        self.assertEqual(field_label, '市名')
    
    def test_skatepark_image_label(self):
        """
        ラベルをパーク名にするテスト
        """
        field_label = self.skatepark._meta.get_field('skatepark_image').verbose_name
        self.assertEqual(field_label, '写真')

    def test_name_max_length_50(self):
        """
        スケートパーク名を最大50字にするテスト
        """
        max_length = self.skatepark._meta.get_field('name').max_length
        self.assertEqual(max_length, 50)

    def test_raises_error_when_name_over_51_characters(self):
        """
        スケートパーク名が51以上の時エラーをあげるテスト
        """
        skatepark = Skatepark(name='t'*51, prefecture='神奈川', city='横浜', skatepark_image='test_image.jpg')
        with self.assertRaises(DataError):
            skatepark.save()

    def test_prefecture_max_length_4(self):
        """
        県名を最大4字にするテスト
        """
        max_length = self.skatepark._meta.get_field('prefecture').max_length
        self.assertEqual(max_length, 4)

    def test_raises_error_when_prefecture_over_5_characters(self):
        """
       県名が5以上の時エラーをあげるテスト
        """
        skatepark = Skatepark(name='Test skatepark', prefecture='かながわ県', city='横浜', skatepark_image='test_image.jpg')
        with self.assertRaises(DataError):
            skatepark.save()

    def test_city_max_length_10(self):
        """
        市名を最大10字にするテスト
        """
        max_length = self.skatepark._meta.get_field('city').max_length
        self.assertEqual(max_length, 10)

    def test_raises_error_when_prefecture_over_5_characters(self):
        """
        市名が11以上の時エラーをあげるテスト
        """
        skatepark = Skatepark(name='Test skatepark', prefecture='神奈川県', city='あ'*11, skatepark_image='test_image.jpg')
        with self.assertRaises(DataError):
            skatepark.save()

    def test_skatepark_object_as_string_is_equal_to_name_plus_prefecture(self):
        """ 
        Skateparkクラスのオブジェクト文字列がユーザーネームと一致するテスト
        """
        self.assertEqual(str(self.skatepark), f'{self.skatepark.name}({self.skatepark.prefecture})')


class PostModelTest(TestCase):
    def setUp(self):
        self.skatepark = Skatepark(name='Test skatepark', prefecture='神奈川', city='横浜', skatepark_image='test_image.jpg')
        self.skatepark.save()
        self.user = User.objects.create(username='testuser', email='test@mail.com', password='testpassword')
        self.user.save()
        self.post = Post(author=self.user, skatepark=self.skatepark, body='Test body')
        self.post.save()

    def test_author_label(self):
        """
        ラベルを投稿者にするテスト
        """
        field_label = self.post._meta.get_field('author').verbose_name
        self.assertEqual(field_label, '投稿者')

    def test_created_at_label(self):
        """
        ラベルを投稿者にするテスト
        """
        field_label = self.post._meta.get_field('created_at').verbose_name
        self.assertEqual(field_label, '投稿日')

    def test_skatepark_label(self):
        """
        ラベルをスケートパークにするテスト
        """
        field_label = self.post._meta.get_field('skatepark').verbose_name
        self.assertEqual(field_label, 'スケートパーク')

    def test_body_label(self):
        """
        ラベルをスケートパークにするテスト
        """
        field_label = self.post._meta.get_field('body').verbose_name
        self.assertEqual(field_label, '内容')

    def test_body_max_length_300(self):
        """
        投稿内容の文字数を最大50字にするテスト
        """
        max_length = self.post._meta.get_field('body').max_length
        self.assertEqual(max_length, 300)

    def test_raises_error_when_name_over_301_characters(self):
        """
        投稿内容の文字数が301以上の時エラーをあげるテスト
        """
        post = Post(author=self.user, skatepark=self.skatepark, body='a'*301)
        with self.assertRaises(DataError):
             post.save()

    def test_skatepark_object_as_string_is_equal_to_name_plus_prefecture(self):
        """ 
        Postクラスのオブジェクト文字列が投稿内容の最初の50字と一致するテスト
        """
        self.assertEqual(str(self.post), self.post.body[:50])