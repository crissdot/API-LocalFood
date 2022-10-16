from django.urls import path
from .api import user_api_view

urlpatterns = [
  path('', user_api_view, name='usuarios'),
]
