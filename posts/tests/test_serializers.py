from django.db.models import Count, Case, When
from django.test import TestCase
from django.contrib.auth.models import User
from unittest.mock import ANY

from posts.models import Post, FavouritePost
from posts.serializers import PostSerializer
from users.models import UserActivity
from users.serializers import UserActivitySerializer


class PostSerializerTestCase(TestCase):
    def setUp(self):
        # authors
        self.author1 = User.objects.create(username='testuser1')
        self.author2 = User.objects.create(username='testuser2')
        self.author3 = User.objects.create(username='testuser3')
        # posts
        self.post1 = Post.objects.create(author_id=self.author1.id, title='test1', body='test123')
        self.post2 = Post.objects.create(author_id=self.author1.id, title='test2', body='test1234')
        # likes
        FavouritePost.objects.create(user=self.author1, post=self.post1, like=True)
        FavouritePost.objects.create(user=self.author2, post=self.post1, like=True)
        FavouritePost.objects.create(user=self.author3, post=self.post1, like=True)
        FavouritePost.objects.create(user=self.author1, post=self.post2, like=True)
        FavouritePost.objects.create(user=self.author2, post=self.post2, like=True)
        FavouritePost.objects.create(user=self.author3, post=self.post2, like=False)

        self.posts = Post.objects.all().annotate(
            likes_count=Count(Case(When(favouritepost__like=True, then=1)))).order_by('id')

    def test_posts_view(self):
        data = PostSerializer(self.posts, many=True).data
        expected_data = [
            {
                'id': self.post1.id,
                'title': 'test1',
                'body': 'test123',
                'author': 'testuser1',
                'created_at': ANY,
                'likes_count': 3,
            },
            {
                'id': self.post2.id,
                'title': 'test2',
                'body': 'test1234',
                'author': 'testuser1',
                'created_at': ANY,
                'likes_count': 2,
            }
        ]
        self.assertEqual(expected_data, data)

    def test_users_view(self):
        self.users = UserActivity.objects.all()
        data = UserActivitySerializer(self.users, many=True).data
        expected_data = [
            {
                'id': self.author1.id,
                'username': 'testuser1',
                'last_login': ANY,
                'last_request': ANY,
            },
            {
                'id': self.author2.id,
                'username': 'testuser2',
                'last_login': ANY,
                'last_request': ANY,
            },
            {
                'id': self.author3.id,
                'username': 'testuser3',
                'last_login': ANY,
                'last_request': ANY,
            }
        ]
        self.assertEqual(expected_data, data)
