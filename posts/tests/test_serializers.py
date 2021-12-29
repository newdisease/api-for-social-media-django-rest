from django.test import TestCase
from django.contrib.auth.models import User

from posts.models import Post, FavouritePost
from posts.serializers import PostSerializer


class PostSerializerTestCase(TestCase):

    def test_post_view(self):
        author1 = User.objects.create(username='testuser1')
        author2 = User.objects.create(username='testuser2')
        author3 = User.objects.create(username='testuser3')

        post1 = Post.objects.create(author_id=author1.id, title='test1', body='test123')
        post2 = Post.objects.create(author_id=author1.id, title='test2', body='test1234')

        FavouritePost.objects.create(user=author1, post=post1, like=True)
        FavouritePost.objects.create(user=author2, post=post1, like=True)
        FavouritePost.objects.create(user=author3, post=post1, like=True)

        FavouritePost.objects.create(user=author1, post=post2, like=True)
        FavouritePost.objects.create(user=author2, post=post2, like=True)
        FavouritePost.objects.create(user=author3, post=post2, like=False)

        data = PostSerializer([post1, post2], many=True).data
        expected_data = [
            {
                'id': post1.id,
                'title': 'test1',
                'body': 'test123',
                'author': 'testuser1',
                'created_at': post1.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                'likes_count': 3
            },
            {
                'id': post2.id,
                'title': 'test2',
                'body': 'test1234',
                'author': 'testuser1',
                'created_at': post2.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                'likes_count': 2
            }
        ]
        self.assertEqual(expected_data, data)
