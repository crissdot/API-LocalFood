from django.urls import path
from .api import CategoryListAPIView, ProductListAPIView

urlpatterns = [
  path('', ProductListAPIView.as_view(), name='productos'),
  path('categorias/', CategoryListAPIView.as_view(), name='categorias'),
]
