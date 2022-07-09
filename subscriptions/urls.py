from django.contrib import admin
from django.urls import path, include

from subscriptions import views

app_name = "subscriptions"

urlpatterns = [
    path('success/', views.SuccessView.as_view(), name='success'),
    path('cancel/', views.CancelView.as_view(), name='cancel'),
]
