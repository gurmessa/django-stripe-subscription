from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect


class SubscriptionRequiredMixin(LoginRequiredMixin):
    """Verify that the user has subscription."""

    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, 'subscription'):
            return HttpResponseRedirect('/')

        return super().dispatch(request, *args, **kwargs)


class ActiveSubscriptionRequiredMixin(LoginRequiredMixin):
    """Verify that the user has an active subscription."""

    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, 'subscription'):
            return HttpResponseRedirect('/')
        elif not request.user.subscription.is_active:
            return HttpResponseRedirect('/')

        return super().dispatch(request, *args, **kwargs)

