from django.urls import path
from .api import LocalFoodAPIView

urlpatterns = [
  path('', LocalFoodAPIView.as_view(), name='negocios')
]
