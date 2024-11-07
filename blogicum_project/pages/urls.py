# blogicum/pages/urls.py
from django.urls import path

from .views import AboutView, RulesView, PrivacyView

app_name = 'pages'

urlpatterns = [
    path('about/', AboutView.as_view(), name='about'),
    path('rules/', RulesView.as_view(), name='rules'),
    path('privacy/', PrivacyView.as_view(), name='privacy'),
]
