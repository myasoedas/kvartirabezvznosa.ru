# blogicum/pages/views.py
from django.shortcuts import render
from django.views.defaults import page_not_found, permission_denied
from django.views.generic import TemplateView


def custom_404_view(request, exception):
    return page_not_found(request, exception, template_name='pages/404.html')


def custom_403_view(request, exception):
    return permission_denied(request, exception,
                             template_name='pages/403csrf.html')


def custom_500_view(request):
    return render(request, 'pages/500.html', status=500)


class AboutView(TemplateView):
    template_name = 'pages/about.html'


class RulesView(TemplateView):
    template_name = 'pages/rules.html'


class PrivacyView(TemplateView):
    template_name = 'pages/privacy.html'
