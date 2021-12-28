from django.test import TestCase
from django.contrib.auth.models import User

from posts.models import Post
from posts.serializers import PostSerializer


class PostSerializerTestCase(TestCase):

    def test_post_view(self):
        author1 = User.objects.create(username='testuser1')
        post1 = Post.objects.create(author_id=author1.id, title='test1', body='test123')
        post2 = Post.objects.create(author_id=author1.id, title='test2', body='test1234')
        data = PostSerializer([post1, post2], many=True).data
        expected_data = [
            {
                'id': post1.id,
                'title': 'test1',
                'body': 'test123',
                'author': 'testuser1',
                'created_at': post1.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                'likes_count': 0
            },
            {
                'id': post2.id,
                'title': 'test2',
                'body': 'test1234',
                'author': 'testuser1',
                'created_at': post2.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                'likes_count': 0
            }
        ]
        self.assertEqual(expected_data, data)
