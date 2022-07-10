from django.test import TestCase
from django.urls import reverse
from django.test import Client
from django.contrib.auth import get_user_model


class HomeViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # create user
        User = get_user_model()
        User.objects.create_user(
            username="test",
            email='test@user.com', 
            password='foo')

    def test_view_redirects_if_not_authorized(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
         
    def test_view_url_exists_at_desired_location(self):
        self.client.login(username='test', password='foo')
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_home_page_returns_correct_html(self):
        self.client.login(username='test', password='foo')
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'subscriptions/home.html')


class CancelViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # create user
        User = get_user_model()
        User.objects.create_user(
            username="test",
            email='test@user.com', 
            password='foo')

    def test_view_redirects_if_not_authorized(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
         
    def test_view_url_exists_at_desired_location(self):
        self.client.login(username='test', password='foo')
        response = self.client.get('/cancel/')
        self.assertEqual(response.status_code, 200)

    def test_home_page_returns_correct_html(self):
        self.client.login(username='test', password='foo')
        response = self.client.get('/cancel/')
        self.assertTemplateUsed(response, 'subscriptions/cancel.html')