from django.contrib import admin
from django.urls import path, include

from subscriptions import views

app_name = "subscriptions"

urlpatterns = [
    path('', views.HomeView.as_view(), name='cancel'),
    path('success/', views.SuccessView.as_view(), name='success'),
    path('cancel/', views.CancelView.as_view(), name='cancel'),
    path(
        'subscription/', 
        views.SubscriptionView.as_view(), 
        name='subscription'
    ),
    path(
        'checkout/', 
        views.CreateCheckoutSessionView.as_view(), 
        name="checkout"
    ),
    path('webhook/', views.stripe_webhook),
]
