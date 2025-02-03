# authentication/tests.py
from rest_framework.test import APITestCase
from rest_framework import status

class AuthTests(APITestCase):
    # Test registration functionality
    def test_registration(self):
        response = self.client.post('/api/auth/register/', {
            'email': 'test@example.com',
            'password': 'testpassword123'
        })
        self.assertEqual(response.status_code, 201)  # Assuming 201 Created status on success
        self.assertIn('token', response.data)  # Checking if the response includes a token

    # Test login functionality
    def test_login(self):
        # First, register the user
        self.client.post('/api/auth/register/', {
            'email': 'test@example.com',
            'password': 'testpassword123'
        })

        # Now, log in with the same credentials
        response = self.client.post('/api/auth/login/', {
            'email': 'test@example.com',
            'password': 'testpassword123'
        })
        
        # Check that the status code is 200, meaning successful login
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.data)  # Checking if the response includes a token

    # Test fetching user info (me endpoint)
    def test_fetch_user_info(self):
        # First, register and login to get a token
        self.client.post('/api/auth/register/', {
            'email': 'test@example.com',
            'password': 'testpassword123'
        })

        # Log in to retrieve the token
        login_response = self.client.post('/api/auth/login/', {
            'email': 'test@example.com',
            'password': 'testpassword123'
        })
        token = login_response.data['token']

        # Use the token to fetch user info
        self.client.credentials(Authorization=f'Bearer {token}')
        response = self.client.get('/api/auth/me/')

        self.assertEqual(response.status_code, 200)  # Expecting success response
        self.assertEqual(response.data['email'], 'test@example.com')  # Ensure that the correct email is returned

    # Test logout functionality
    def test_logout(self):
        # First, register and log in to get a token
        self.client.post('/api/auth/register/', {
            'email': 'test@example.com',
            'password': 'testpassword123'
        })

        # Log in to retrieve the token
        login_response = self.client.post('/api/auth/login/', {
            'email': 'test@example.com',
            'password': 'testpassword123'
        })
        token = login_response.data['token']

        # Now, log out
        self.client.credentials(Authorization=f'Bearer {token}')
        response = self.client.post('/api/auth/logout/')

        # Expecting a 200 status code for successful logout
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.data)  # Checking for success message
        self.assertEqual(response.data['message'], 'Logout successful')  # Example response message
