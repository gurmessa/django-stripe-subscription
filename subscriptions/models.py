from django.db import models
from django.contrib.auth import get_user_model
from .constants import SUBSCRIPTION_CHOICES


class Subscription(models.Model):
    user = models.OneToOneField(to=get_user_model(), on_delete=models.CASCADE)
    subscription_id = models.CharField(max_length=255)
    status = models.CharField(max_length=50, choices=SUBSCRIPTION_CHOICES)
    start_date = models.DateTimeField()
    ended_at = models.DateTimeField(null=True, blank=True)
    trial_end = models.DateTimeField()
    trial_start = models.DateTimeField()
    canceled_at = models.DateTimeField(null=True, blank=True)
    current_period_end = models.DateTimeField()
    current_period_start = models.DateTimeField()

    @property
    def is_active(self):
        """check if the subscrition is active or on trial period"""
        return self.status == 'active' or self.status == 'trialing'