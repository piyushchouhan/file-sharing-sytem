from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class OpsUserTestCase(TestCase):
    def setUp(self):
        self.signup_url = reverse('ops_user_signup')
        self.valid_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'password123',
            'confirmation': 'password123',
        }
        self.invalid_data = {
            'username': 'testuser2',
            'email': 'testuser2@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'password123',
            'confirmation': 'wrongpassword',
        }

    def test_signup_valid_data(self):
        response = self.client.post(self.signup_url, self.valid_data)
        self.assertEqual(response.status_code, 302)  # Check for redirect status code
        self.assertRedirects(response, reverse('index'))  # Ensure redirection to index
        self.assertTrue(User.objects.filter(username='testuser').exists())  # Check user creation
        self.assertEqual(User.objects.get(username='testuser').is_active, True)  # Check if user is active

    def test_signup_password_mismatch(self):
        response = self.client.post(self.signup_url, self.invalid_data)
        self.assertEqual(response.status_code, 200)  # Check for successful render of the page
        self.assertContains(response, "Passwords must match.")  # Ensure error message is shown
        self.assertFalse(User.objects.filter(username='testuser2').exists())  # Ensure user is not created

    def test_signup_username_taken(self):
        # First, create a user with the same username
        User.objects.create_user(username='testuser', email='existing@example.com', password='password123')
        response = self.client.post(self.signup_url, self.valid_data)
        self.assertEqual(response.status_code, 200)  # Check for successful render of the page
        self.assertContains(response, "Username already taken.")  # Ensure error message is shown
