from django.test import TestCase, Client
import json


class UsersTestCase(TestCase):

    def authenticate_user(self):
        c = Client()
        data = {
            'username': 'testuser1',
            'email': 'testuser1@gmail.com',
            'password': 'testuser1',
            'confirmed_password': 'testuser1'
        }
        c.post('/api/users/', data=data, content_type='application/json')
        data = {
            'username': 'testuser1',
            'password': 'testuser1',
        }
        response = c.post('/api/auth/', data=data, content_type='application/json')
        return response.json()['token']

    def test_get_posts(self):
        c = Client()
        response = c.get('/api/posts/')
        self.assertEqual(response.status_code, 200)

    def test_post_blog(self):
        c = Client()
        token = self.authenticate_user()

        data = {
            'name': 'my test post',
            'body': 'my test body'
        }
        header = {'HTTP_AUTHORIZATION': f' {token}'}
        response = c.post('/api/posts/', data=data, content_type='application/json', **header)
        self.assertEqual(response.status_code, 401)

        data = {
            'name': 'my test post',
            'body': 'my test body'
        }
        response = c.post('/api/posts/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 401)

        data = {
            'name': 'my test post',
            'body': 'my test body'
        }
        header = {'HTTP_AUTHORIZATION': f'Token {token}'}
        response = c.post('/api/posts/', data=data, content_type='application/json', **header)
        self.assertEqual(response.status_code, 201)
