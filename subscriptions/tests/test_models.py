from datetime import datetime, timedelta
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.conf import settings
from subscriptions.models import Subscription


class SubscriptionTests(TestCase):

    def test_create_subscription(self):
        User = get_user_model()
        user = User.objects.create_user(
            username="test",
            email='test@user.com', 
            password='foo')

        current_date = datetime.now()
        trial_end_date = current_date + \
            timedelta(days=settings.STRIPE_TRIAL_PERIOD_DAYS)

        subscription = Subscription.objects.create(
            status="trialing",
            user=user,
            start_date=current_date,
            trial_start=current_date,
            trial_end=trial_end_date,
            current_period_start=current_date,
            current_period_end=trial_end_date
        )

        self.assertEqual(subscription.user, user)
        self.assertEqual(subscription.trial_start, current_date)
        self.assertEqual(subscription.trial_end, trial_end_date)
        self.assertEqual(subscription.current_period_start, current_date)
        self.assertEqual(subscription.current_period_end, trial_end_date)
        self.assertEqual(subscription.ended_at, None)
        self.assertEqual(subscription.canceled_at, None)

        subscription.status = 'canceled'
        subscription.canceled_at = trial_end_date
        subscription.save()

        self.assertEqual(subscription.status, 'canceled')
        self.assertEqual(subscription.canceled_at, trial_end_date)