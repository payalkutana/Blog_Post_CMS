from django.test import TestCase
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
from blog.models import Post, Like

class BlogAppAPITestCases(APITestCase):
    def setUp(self):
        self.client = APIClient()

        #create user
        self.user = User.objects.create_user(username='testuser1', password='Testpass1')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        #create public post
        self.post = Post.objects.create(user=self.user, title='test blog', description = 'test description', content='test content', is_public=True)

        #create Like
        self.like = Like.objects.create(post=self.post, user=self.user)

    def test_create_user(self):
        self.client.credentials()
        data = {'username': 'testuser2', 'password': 'Testpass2', 'email':'dummy@gmail.com'}
        res = self.client.post('/accounts', data, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='testuser2').exists())

    def test_login_user(self):
        self.client.credentials()
        data = {'username': 'testuser2', 'password': 'Testpass2'}
        res = self.client.post('/accounts/login', data, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('token', res.data)

    def test_get_user(self):
        res = self.client.get('/me')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['username'], 'testuser2')
        
    def test_update_user(self):
        data = {'username': 'testuser2', 'password': 'Testpass2', 'email':'testuser2@gmail.com'}
        res = self.client.put('/accounts/update', data, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(User.objects.filter(email='testuser2@gmail.com').exists())

    def test_delete_user(self):
        res = self.client.delete('/accounts/delete')
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(username='testuser2').exists())

    def test_create_post(self):
        data = {'user': self.user.id, 'title': 'test blog 1', 'description' : 'test description', 'content':'test content', 'is_public':True}
        res = self.client.post('/blog', data, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Post.objects.filter(title='test blog 1').exists())

    def test_get_posts(self):
        res = self.client.get('/blog')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_post(self):
        res = self.client.get(f'/blog/{self.post.id}')
        self.assertEqual(res.status_code, status.HTTP_200_OK)