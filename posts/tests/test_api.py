import json
from unittest.mock import ANY
from django.contrib.auth.models import User
from django.db.models import Count, Case, When
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from posts.models import Post, FavouritePost
from posts.serializers import PostSerializer


class PostsApiTestCase(APITestCase):
    def setUp(self):
        # authors
        self.author1 = User.objects.create(username='testuser1')
        self.author2 = User.objects.create(username='testuser2')
        self.author3 = User.objects.create(username='testuser3')
        # posts
        self.post1 = Post.objects.create(author_id=self.author1.id, title='test1', body='test123')
        self.post2 = Post.objects.create(author_id=self.author1.id, title='test2', body='test1234')
        self.post3 = Post.objects.create(author_id=self.author1.id, title='test3', body='test12345')

    def test_get_all_posts(self):
        url = reverse('posts:post-list')
        response = self.client.get(url)
        posts = Post.objects.all().annotate(
            likes_count=Count(Case(When(favouritepost__like=True, then=1)))).order_by('id')
        serializer_data = PostSerializer(posts, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_one_posts(self):
        url = reverse('posts:post-detail', args=(self.post1.id,))
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual({'id': self.post1.id,
                          'title': 'test1',
                          'body': 'test123',
                          'author': 'testuser1',
                          'created_at': ANY,
                          'likes_count': 0
                          }, response.data)

    def test_create_post(self):
        self.assertEqual(3, Post.objects.all().count())
        url = reverse('posts:post-list')
        self.client.force_authenticate(self.author1)
        data = {
            "title": "test4",
            "body": "test123456"
        }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(4, Post.objects.all().count())

    def test_update_own_post(self):
        url = reverse('posts:post-detail', args=(self.post1.id,))
        self.client.force_authenticate(self.author1)
        data = {
            "title": "test1 UPDATED",
            "body": "test123456 UPDATED"
        }
        json_data = json.dumps(data)
        response = self.client.put(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.post1.refresh_from_db()
        self.assertEqual("test1 UPDATED", self.post1.title)
        self.assertEqual("test123456 UPDATED", self.post1.body)

    def test_update_other_post(self):
        url = reverse('posts:post-detail', args=(self.post1.id,))
        self.client.force_authenticate(self.author2)
        data = {
            "title": "test1 UPDATED",
            "body": "test123456 UPDATED"
        }
        json_data = json.dumps(data)
        response = self.client.put(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.post1.refresh_from_db()
        self.assertEqual("test1", self.post1.title)
        self.assertEqual("test123", self.post1.body)

    def test_delete_own_post(self):
        self.assertEqual(3, Post.objects.all().count())
        url = reverse('posts:post-detail', args=(self.post1.id,))
        self.client.force_authenticate(self.author1)
        response = self.client.delete(url, content_type='application/json')
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(2, Post.objects.all().count())

    def test_delete_other_post(self):
        self.assertEqual(3, Post.objects.all().count())
        url = reverse('posts:post-detail', args=(self.post1.id,))
        self.client.force_authenticate(self.author2)
        response = self.client.delete(url, content_type='application/json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(3, Post.objects.all().count())


class FavouritePostApiTestCase(APITestCase):
    def setUp(self):
        # authors
        self.author1 = User.objects.create(username='testuser1')
        self.author2 = User.objects.create(username='testuser2')
        self.author3 = User.objects.create(username='testuser3')
        # posts
        self.post1 = Post.objects.create(author_id=self.author1.id, title='test1', body='test123')
        self.post2 = Post.objects.create(author_id=self.author1.id, title='test2', body='test1234')
        self.post3 = Post.objects.create(author_id=self.author1.id, title='test3', body='test12345')

    def test_like_post(self):
        url = reverse('posts:favouritepost-detail', args=(self.post1.id,))
        self.client.force_authenticate(self.author1)
        response = self.client.patch(url, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.post1.refresh_from_db()
        relation = FavouritePost.objects.get(user=self.author1, post=self.post1)
        self.assertTrue(relation.like)
