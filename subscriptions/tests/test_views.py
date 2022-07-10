from datetime import datetime, timedelta
from django.test import TestCase
from django.urls import reverse
from django.test import Client
from django.contrib.auth import get_user_model
from django.conf import settings
from subscriptions.models import Subscription


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


class SuccessView(TestCase):
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
        response = self.client.get('/success/')
        self.assertEqual(response.status_code, 200)

    def test_success_page_returns_correct_html(self):
        self.client.login(username='test', password='foo')
        response = self.client.get('/success/')
        self.assertTemplateUsed(response, 'subscriptions/success.html')


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

    def test_cancel_page_returns_correct_html(self):
        self.client.login(username='test', password='foo')
        response = self.client.get('/cancel/')
        self.assertTemplateUsed(response, 'subscriptions/cancel.html')


class SubscriptionView(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()

        # create a user that has no stripe subcription
        user1 = User.objects.create_user(
            username="test",
            email='test@user.com', 
            password='foo')

        # create a user that has stripe subcription
        user2 = User.objects.create_user(
            username="test2",
            email='test2@user.com', 
            password='foo')

        current_date = datetime.now()
        trial_end_date = current_date + \
            timedelta(days=settings.STRIPE_TRIAL_PERIOD_DAYS)
        # create subscription for user 2
        Subscription.objects.create(
            status="trialing",
            user=user2,
            start_date=current_date,
            trial_start=current_date,
            trial_end=trial_end_date,
            current_period_start=current_date,
            current_period_end=trial_end_date
        )

    def test_view_redirects_if_not_authorized(self):
        response = self.client.get('/subscription/')
        self.assertEqual(response.status_code, 302)

    def test_view_redirects_to_home_if_not_subscribed(self):
        self.client.login(username='test', password='foo')
        response = self.client.get('/subscription/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/')

    def test_view_url_exists_at_desired_location_for_subscribed_user(self):
        self.client.login(username='test2', password='foo')
        response = self.client.get('/subscription/')
        self.assertEqual(response.status_code, 200)

    def test_subscription_page_returns_correct_html(self):
        self.client.login(username='test2', password='foo')
        response = self.client.get('/subscription/')
        self.assertTemplateUsed(response, 'subscriptions/subscription.html')