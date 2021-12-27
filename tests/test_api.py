import json

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse

from posts.models import Post
from django.contrib.auth import get_user_model

from posts.serializers import PostSerializer


class PostsApiTestCase(APITestCase):

    def setUp(self):
        User = get_user_model()
        self.user_1 = User.objects.create_user(
            username='user',
            password='user1234'
        )
        self.post_1 = Post.objects.create(
            author_id=1,
            title='test',
            body='test123')
        self.post_2 = Post.objects.create(
            author_id=1,
            title='test1',
            body='test1234')

    def test_get_all_posts(self):
        url = reverse('posts:post-list')
        response = self.client.get(url)
        serializer_data = PostSerializer([self.post_1, self.post_2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_detail_post(self):
        url = reverse('posts:post-detail', args=f'{self.post_1.pk}')
        response = self.client.get(url)
        serializer_data = PostSerializer(self.post_1).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_create_post(self):
        self.assertEqual(2, Post.objects.all().count())
        url = reverse('posts:post-list')
        data = {
            "author": 1,
            "title": "test create",
            "body": "test body"
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user_1)
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(3, Post.objects.all().count())

    def test_update_post(self):
        self.assertEqual(2, Post.objects.all().count())
        url = reverse('posts:post-detail', args=(self.post_1.id,))
        data = {
            "author": self.user_1.id,
            "title": self.post_1.title,
            "body": "test body updated"
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user_1)
        response = self.client.put(url, data=json_data, content_type='application/json')
        self.post_1.refresh_from_db()
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual("test body updated", f'{self.post_1.body}')
