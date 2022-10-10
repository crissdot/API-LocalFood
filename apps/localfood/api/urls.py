from django.urls import path
from .api import LocalFoodAPIView, LocalFoodDetailAPIView

urlpatterns = [
  path('', LocalFoodAPIView.as_view(), name='negocios'),
  path('<int:pk>/', LocalFoodDetailAPIView.as_view(), name='negocio'),
]
