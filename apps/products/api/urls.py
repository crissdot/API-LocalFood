from django.urls import path
from .api import CategoryListAPIView, ProductListAPIView, ProductDetailApiView

urlpatterns = [
  path('', ProductListAPIView.as_view(), name='productos'),
  path('<int:pk>/', ProductDetailApiView.as_view(), name='producto'),
  path('categorias/', CategoryListAPIView.as_view(), name='categorias'),
]
