from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class SuccessView(LoginRequiredMixin, TemplateView):
    template_name = "subscriptions/success.html"
