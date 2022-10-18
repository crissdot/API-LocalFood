from django.urls import path
from .api import CategoryListAPIView

urlpatterns = [
  path('categorias/', CategoryListAPIView.as_view(), name='categorias'),
]
