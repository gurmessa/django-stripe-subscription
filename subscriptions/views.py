from datetime import datetime
import stripe
from django.shortcuts import render
from django.views.generic import TemplateView
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.http import JsonResponse, HttpResponse
from .models import Subscription

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


@csrf_exempt
def stripe_webhook(request):
    """ Strip webhook function"""
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    print('Handled event type {}'.format(event['type']))

    # customer subscription event types
    SUBSCRIPTION_EVENT_TYPES = [
        "customer.subscription.created",
        "customer.subscription.deleted",
        "customer.subscription.pending_update_applied",
        "customer.subscription.pending_update_expired",
        "customer.subscription.updated"
    ] 

    if event['type'] in SUBSCRIPTION_EVENT_TYPES:
        subscription_obj = event['data']['object']
        user = get_user_model().objects.get(
            stripe_customer_id=subscription_obj.get('customer'))
        if event['type'] == "customer.subscription.created":
            subscription = Subscription() 
            subscription.user = user
            subscription.subscription_id = subscription_obj.get('id')
        else:
            subscription = Subscription.objects.get(
                user=user,
                subscription_id=subscription_obj.get('id'))
        
        subscription.status = subscription_obj.get('status')
        subscription.start_date = datetime.utcfromtimestamp(
            subscription_obj.get('start_date'))
        if subscription_obj.get('ended_at'):
            subscription.ended_at = datetime.utcfromtimestamp(
                subscription_obj.get('ended_at'))
        subscription.trial_end = datetime.utcfromtimestamp(
            subscription_obj.get('trial_end')) 
        subscription.trial_start = datetime.utcfromtimestamp(
            subscription_obj.get('trial_start'))
        if subscription_obj.get('canceled_at'):
            subscription.canceled_at = datetime.utcfromtimestamp(
                subscription_obj.get('canceled_at')) 
        subscription.current_period_end = datetime.utcfromtimestamp(
            subscription_obj.get('current_period_end'))
        subscription.current_period_start = datetime.utcfromtimestamp(
            subscription_obj.get('current_period_start'))
        subscription.save()

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        # Fetch all the required data from session
        client_reference_id = session.get('client_reference_id')
        stripe_customer_id = session.get('customer')
        stripe_subscription_id = session.get('subscription')

        user = get_user_model().objects.get(id=client_reference_id)
        user.stripe_customer_id = stripe_customer_id
        user.save()
 
    return HttpResponse(status=200)

