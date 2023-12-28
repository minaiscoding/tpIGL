from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Utilisateurs
from django.urls import reverse

'''class LoginTestCase(TestCase):
    def setUp(self):
        # Create a test user for the Utilisateurs model
        self.user = Utilisateurs.objects.create(
            NomUtilisateur='testuser',
            Email='testuser@example.com',
            MotDePasse='testpassword',
            Role='user'
        )

        self.client = APIClient()
        
    def test_login_successful(self):
       url = reverse('token-view')
       response = self.client.post(url, {'NomUtilisateur': 'testuser', 'MotDePasse': 'testpassword'})
       print(response.data)
       self.assertEqual(response.status_code, status.HTTP_200_OK)
       self.assertIn('token', response.data)
    
    # Check if user information is directly available in validated_data
       user = response.data.get('user')
       self.assertIsNotNone(user)
 
    def test_login_invalid_credentials(self):
        # Test login with invalid credentials
        response = self.client.post('token/', {'NomUtilisateur': 'testuser', 'MotDePasse': 'wrongpassword'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # Add more assertions as needed'''
