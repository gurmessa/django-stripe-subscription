import stripe
from django.shortcuts import render
from django.views.generic import TemplateView
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import redirect

stripe.api_key = settings.STRIPE_SECRET_KEY


class SuccessView(LoginRequiredMixin, TemplateView):
    template_name = "subscriptions/success.html"


class CancelView(LoginRequiredMixin, TemplateView):
    template_name = "subscriptions/cancel.html"


class CreateCheckoutSessionView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            customer_email=request.user.email,
            client_reference_id=request.user.id,
            line_items=[
                {
                    'price': settings.STRIPE_PRICE_ID,
                    'quantity': 1,
                },
            ],
            mode='subscription',
            subscription_data={
                "trial_period_days": settings.STRIPE_TRIAL_PERIOD_DAYS
            },
            success_url=settings.DOMAIN_URL + '/success/',
            cancel_url=settings.DOMAIN_URL + '/cancel/',
        )
        return redirect(checkout_session.url)