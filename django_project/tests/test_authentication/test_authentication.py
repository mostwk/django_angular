from django.test import TestCase, Client
import json
# Create your tests here.


class UsersTestCase(TestCase):

    def test_get_all_users(self):
        c = Client()
        response = c.get('/api/users/')
        self.assertEqual(response.status_code, 200)

    def test_post_user_normal(self):
        c = Client()
        data = {
            'username': 'testuser1',
            'email': 'testuser1@gmail.com',
            'password': 'testuser1',
            'confirmed_password': 'testuser1'
        }
        response = c.post('/api/users/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 201)

        response = c.get('/api/users/testuser1/')
        self.assertEqual(response.status_code, 200)

    def test_post_user_with_errors(self):
        c = Client()
        data = {
            'username': '',
            'email': 'testuser1@gmail.com',
            'password': 'testuser1',
            'confirmed_password': 'testuser1'
        }
        response = c.post('/api/users/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)

        data = {
            'username': 'testuser1',
            'email': '',
            'password': 'testuser1',
            'confirmed_password': 'testuser1'
        }
        response = c.post('/api/users/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)

        data = {
            'username': 'testuser1',
            'email': 'testuser1@gmail.com',
            'password': '',
            'confirmed_password': 'testuser1'
        }
        response = c.post('/api/users/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)

        data = {
            'username': 'testuser1',
            'email': 'testuser1@gmail.com',
            'password': 'testuser1',
            'confirmed_password': ''
        }
        response = c.post('/api/users/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)

        data = {
            'username': 'testuser1',
            'email': 'testuser1@gmail.com',
            'password': 'testuser1',
            'confirmed_password': 'testuser'
        }
        response = c.post('/api/users/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)

        data = {
            'username': 'testuser1',
            'email': 'testuser1@gmail',
            'password': 'testuser1',
            'confirmed_password': 'testuser1'
        }
        response = c.post('/api/users/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_post_auth(self):
        c = Client()
        data = {
            'username': 'testuser1',
            'email': 'testuser1@gmail.com',
            'password': 'testuser1',
            'confirmed_password': 'testuser1'
        }
        response = c.post('/api/users/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 201)

        data = {
            'username': 'testuser1',
            'password': 'testuser1'
        }
        response = c.post('/api/auth/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)

        data = {
            'username': '',
            'password': 'testuser1'
        }
        response = c.post('/api/auth/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)

        data = {
            'username': 'testuser1',
            'password': ''
        }
        response = c.post('/api/auth/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)

        data = {
            'username': '',
            'password': ''
        }
        response = c.post('/api/auth/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
