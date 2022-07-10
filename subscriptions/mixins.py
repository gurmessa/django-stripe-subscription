from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect


class SubscriptionRequiredMixin(LoginRequiredMixin):
    """Verify that the user has subscription."""

    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, 'subscription'):
            return HttpResponseRedirect('/')

        return super().dispatch(request, *args, **kwargs)

